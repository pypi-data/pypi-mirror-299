import os
import requests
import sys
import math
import traceback
from bson import ObjectId
import shutil
import zipfile
import tarfile
import yaml
from pycocotools.coco import COCO
from matrice.session import Session
from matrice.models import Model
from matrice import rpc

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ActionTracker:

    def __init__(self, action_id=None):
        try:
            session = Session()
            self.rpc = session.rpc

            if action_id is not None:
                self.action_id = ObjectId(action_id)
                self.action_id_str = str(self.action_id)
                url = f"/v1/project/action/{self.action_id_str}/details"
                self.action_doc = self.rpc.get(url)['data']
                print(self.action_doc)
                self.action_details = self.action_doc['actionDetails']
                self.action_type = self.action_doc['action']

                # Will be updated
                if self.action_type in ("model_train", "model_eval"):
                    self._idModel = self.action_doc['_idService']
                    self._idModel_str = str(self._idModel)
                elif self.action_type == "deploy_add":
                    self._idModel = self.action_details['_idModelDeploy']
                    self._idModel_str = str(self._idModel)
                else:
                    self._idModel = self.action_details['_idModel']
                    self._idModel_str = str(self._idModel)
            else:
                self.action_id = None
                print("ActionTracker initialized. but No action found")

            project_id = self.action_doc["_idProject"]
            #port=self.action_doc["port"]

            try:
                session.update_session(project_id = project_id)
                self.session = session
            except Exception as e:
                print('update project error', e)

            try:
                print(self.get_job_params())
                self.checkpoint_path, self.pretrained = self.get_checkpoint_path(self.get_job_params())
            except Exception as e:
                print('get checkpoint error', e)

        except Exception as e:
            print('PAR', e)
            self.log_error(__file__, '__init__', str(e))
            self.update_status("error", "error", "Initialization failed")
            sys.exit(1)

    def log_error(self, filename, function_name, error_message):
        """ "This function logs error to be-system."""
        traceback_str = traceback.format_exc().rstrip()
        # Constructing the exception information dictionary
        log_err = {
            "serviceName": "Python-Common",
            "stackTrace": traceback_str,
            "errorType": "Internal",
            "description": error_message,
            "fileName": filename,
            "functionName": function_name,
            "moreInfo": {},
        }
        r = rpc.RPC()
        error_logging_route = "/internal/v1/system/log_error"
        #r.post(url=error_logging_route, data=log_err)
        print("An exception occurred. Logging the exception information:")


    def download_model_1(self, model_save_path, presigned_url):
        try:
            response = requests.get(presigned_url)
            if response.status_code == 200:
                with open(model_save_path, 'wb') as file:
                    file.write(response.content)
                print("Download Successful")
                return True
            else:
                print(f"Download failed with status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(__file__, 'download_model_1', str(e))
            print(f"Exception in download_model_1: {str(e)}")
            sys.exit(1)

    def get_checkpoint_path(self, model_config):
        try:
            checkpoint_type = model_config.get("checkpoint_type", "predefined")
            model_checkpoint = model_config.get("model_checkpoint", "auto")
            checkpoint_dir = "./checkpoints"
            os.makedirs(checkpoint_dir, exist_ok=True)

            if checkpoint_type == "model_id":
                if model_checkpoint.lower() not in ["", "none", "auto"]:
                    model_save_path = os.path.abspath(f"{checkpoint_dir}/last.pt")
                    return self.download_trained_model_checkpoint(model_save_path, model_checkpoint), True 
                else:
                    print(f"model_checkpoint {model_checkpoint} is one of [none, auto, ''] it should be a model id")
                    return None, False 
                
            elif checkpoint_type == "predefined":
                if model_checkpoint.lower() == "auto":
                    return None, True 
                elif model_checkpoint.lower() in ["none", ""]:
                    return None, False 
                else:
                    print(f"model_checkpoint {model_checkpoint} not from [none, auto, '']")
                    return None, False 
            else:
                print(f"checkpoint_type {checkpoint_type} not from [model_id, predefined]")
                return None, False 

        except Exception as e:
            self.log_error(__file__, 'get_checkpoint_path', str(e))
            print(f"Exception in get_checkpoint_path: {str(e)}")
            return None, False
    
    def download_trained_model_checkpoint(self, model_save_path, model_id): #TODO test this func and update it with the updated SDK
        try:
            model_sdk = Model(self.session, model_id)
            model_save_path = model_sdk.download_model(model_save_path)
            
            if model_save_path:
                print("Download Successful")
                return model_save_path
            else:
                print(f"Download failed")
                raise Exception(f"Failed to download model from presigned_url")
        except Exception as e:
                    self.log_error(__file__, 'download_trained_model_checkpoint', str(e))
                    print(f"Exception in download_trained_model_checkpoint: {str(e)}")
                    sys.exit(1)

    def get_job_params(self):
        try:
            self.jobParams = self.action_doc['jobParams']
            return dotdict(self.jobParams)
        except Exception as e:
            self.log_error(__file__, 'get_job_params', str(e))
            print(f"Exception in get_job_params: {str(e)}")
            self.update_status("error", "error", "Failed to get job parameters")
            sys.exit(1)

    def update_status(self, stepCode, status, status_description):
        try:
            print(status_description)
            url = f"/v1/project/action"

            payload = {
                "_id": self.action_id_str,
                "action": self.action_type,
                "serviceName": self.action_doc['serviceName'],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }

            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            self.log_error(__file__, 'update_status', str(e))
            print(f"Exception in update_status: {str(e)}")
            if status == "error":
                sys.exit(1)

    def log_epoch_results(self, epoch, epoch_result_list):
        try:
            epoch_result_list = self.round_metrics(epoch_result_list)
            model_log_payload = {
                "_idModel": self._idModel_str,
                "_idAction": self.action_id_str,
                "epoch": epoch,
                "epochDetails": epoch_result_list,
            }

            headers = {'Content-Type': 'application/json'}
            path = f"/v1/model_logging/model/{self._idModel_str}/train_epoch_log"

            self.rpc.post(path=path, headers=headers, payload=model_log_payload)
        except Exception as e:
            self.log_error(__file__, 'log_epoch_results', str(e))
            print(f"Exception in log_epoch_results: {str(e)}")
            self.update_status("error", "error", "Failed to log epoch results")
            sys.exit(1)
            
    def round_metrics(self, epoch_result_list):
        for metric in epoch_result_list:
            if metric["metricValue"] is not None:
                # Check if the value is within JSON-compliant range
                if math.isinf(metric["metricValue"]) or math.isnan(metric["metricValue"]):
                    metric["metricValue"] = 0
                else:
                    metric["metricValue"] = round(metric["metricValue"], 4)
                if metric["metricValue"] == 0:
                    metric["metricValue"] = 0.0001
        return epoch_result_list
    
    def upload_checkpoint(self, checkpoint_path, model_type="trained"):
        try:
            if self.action_type == "model_export" and model_type == "exported":
                model_id = self.action_doc['_idService']
            else:
                model_id = self._idModel_str

            presigned_url = self.rpc.get(path=f"/v1/model/get_model_upload_path", params={
                "modelID": model_id,
                "modelType": model_type,
                "filePath": checkpoint_path.split("/")[-1],
                "expiryTimeInMinutes": 59
            })['data']

            with open(checkpoint_path, 'rb') as file:
                response = requests.put(presigned_url, data=file)

            if response.status_code == 200:
                print("Upload Successful")
                return True
            else:
                print(f"Upload failed with status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(__file__, 'upload_checkpoint', str(e))
            print(f"Exception in upload_checkpoint: {str(e)}")
            self.update_status("error", "error", "Checkpoint upload failed")
            sys.exit(1)

    def download_model(self, model_path, model_type="trained"):
        try:
            model_id = self._idModel_str

            if model_type == "trained":
                presigned_url = self.rpc.post(path=f"/v1/model/get_model_download_path", payload={
                    "modelID": model_id,
                    "modelType": model_type,
                    "expiryTimeInMinutes": 59
                })['data']

            if model_type == "exported":
                presigned_url = self.rpc.post(path=f"/v1/model/get_model_download_path", payload={
                    "modelID": model_id,
                    "modelType": model_type,
                    "expiryTimeInMinutes": 59,
                    "exportFormat": self.action_details['runtimeFramework'],
                })['data']

            response = requests.get(presigned_url)

            if response.status_code == 200:
                with open(model_path, 'wb') as file:
                    file.write(response.content)
                print("Download Successful")
                return True
            else:
                print(f"Download failed with status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_error(__file__, 'download_model', str(e))
            print(f"Exception in download_model: {str(e)}")
            self.update_status("error", "error", "Model download failed")
            sys.exit(1)

    def save_evaluation_results(self, list_of_result_dicts):
        try:
            url = f'/v1/model/add_eval_results'

            Payload = {
                "_idModel": self._idModel,
                "_idDataset": self.action_details['_idDataset'],
                "_idProject": self.action_doc['_idProject'],
                "isOptimized": self.action_details.get('isOptimized', False),
                "runtimeFramework": self.action_details.get('runtimeFramework', "Pytorch"),
                "datasetVersion": self.action_details['datasetVersion'],
                "splitTypes": '',
                "evalResults": list_of_result_dicts
            }

            self.rpc.post(path=url, payload=Payload)
        except Exception as e:
            self.log_error(__file__, 'save_evaluation_results', str(e))
            print(f"Exception in save_evaluation_results: {str(e)}")
            self.update_status("error", "error", "Failed to save evaluation results")
            sys.exit(1)

    def add_index_to_category(self, indexToCat):
        try:
            url = f'/v1/model/{self._idModel}/update_index_to_cat'
            payload = {"indexToCat": indexToCat}
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            self.log_error(__file__, 'add_index_to_category', str(e))
            print(f"Exception in add_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to add index to category")
            sys.exit(1)

    def get_model_train(self, is_exported=False):
        try:
            url = "/v1/model/model_train/" + str(self._idModel_str)
            if is_exported:
                url = f"/v1/model/get_model_train_by_export_id?exportId={self._idModel_str}"
            model_train_doc = self.rpc.get(url)['data']
            return model_train_doc
        
        except Exception as e:
            self.log_error(__file__, 'get_model_train', str(e))
            print(f"Exception in get_model_train: {str(e)}")
            self.update_status("error", "error", "Failed to get model train")
            sys.exit(1)

    def get_index_to_category(self, is_exported=False):
        try:
            model_train_doc = self.get_model_train(is_exported=is_exported)
            self.index_to_category = model_train_doc.get('indexToCat', {})
            return self.index_to_category
        except Exception as e:
            self.log_error(__file__, 'get_index_to_category', str(e))
            print(f"Exception in get_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to get index to category")
            sys.exit(1)

class LocalActionTracker(ActionTracker): # TODO: remove it and use the TestingActionTracker in testing.py

    def __init__(self, action_type , model_name , model_arch , output_type ,action_id=None, local_model_path=None,):
        session = Session()
        self.rpc = session.rpc
        self.local_model_path = local_model_path
        self.model_name = model_name
        self.model_arch = model_arch
        self.output_type = output_type
        self.checkpoint_path, self.pretrained = self.get_checkpoint_path()
        self.action_type = action_type
        assert action_id is None, "Action ID should be None for LocalActionTracker"
        self.action_doc = self.mock_action_doc()
        self.action_details = self.action_doc['actionDetails']

        # Download the dataset and prepare it for the action type in the specific format
        self.prepare_dataset()
        self.create_config()

    def mock_action_doc(self, input_type='image'):
        try:
            api_url = f"/v1/system/get_dataset_url?inputType={input_type}&outputType={self.output_type}"
            response = self.rpc.get(
                path=api_url,
                params={
                    "inputType": input_type,
                    "outputType": self.output_type
                }
            )
            if response and 'data' in response:
                mock_dataset = response['data']
            else:
                raise ValueError("Invalid response from the API call")

            action_details = {
            '_idModel': 'mocked_model_id',
            'runtimeFramework': 'Pytorch',
            'datasetVersion': 'v1.0',
            'dataset_url': mock_dataset,
            'project_type': self.output_type,
            'input_type': input_type,
            'output_type': self.output_type
           }
            # Store _idModel as an instance variable
            self._idModel = action_details['_idModel']
            return {
                'actionDetails': action_details,
                'action': self.action_type,
                'serviceName': 'mocked_service_name',
                '_idProject': 'mocked_project_id'
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def prepare_dataset(self):
        dataset_images_dir = 'workspace/dataset'

        if os.path.exists(dataset_images_dir):
            print(f"Dataset directory {dataset_images_dir} already exists. Skipping download and preparation.")
        else:
            dataset_url = self.action_details.get('dataset_url')
            project_type = self.action_details.get('project_type')
            input_type = self.action_details.get('input_type')
            output_type = self.action_details.get('output_type')

            print(f"Preparing dataset from {dataset_url} for project type {project_type} with input type {input_type} and output type {output_type}")

            dataset_dir = 'workspace/dataset'
            os.makedirs(dataset_dir, exist_ok=True)
            self.download_and_extract_dataset(dataset_url, dataset_dir)

            # Prepare the dataset according to the project type
            if project_type == 'classification':
                self.prepare_classification_dataset(dataset_dir)
        
            elif project_type == 'detection':
                if self.model_name=='Yolov8':
                    self.prepare_yolo_dataset(dataset_dir)
                else:
                    self.prepare_detection_dataset(dataset_dir)
            else:
                print(f"Unsupported project type: {project_type}")


    def download_and_extract_dataset(self, dataset_url, dataset_dir):
        # Extract the file name from the URL
        file_name = os.path.basename(dataset_url)
        local_file_path = os.path.join(dataset_dir, file_name)

        try:
            # Download the file
            with requests.get(dataset_url, stream=True) as r:
                r.raise_for_status()

                print(f"Response status code: {r.status_code}")
                print(f"Response headers: {r.headers}")

                content_type = r.headers.get('Content-Type', 'Unknown')
                print(f"Content-Type: {content_type}")

                # Save the file
                with open(local_file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            print(f"File downloaded successfully from {dataset_url}")
            print(f"Saved as: {local_file_path}")

            # Extract the file based on its extension
            if file_name.endswith('.zip'):
                with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
                    zip_ref.extractall(dataset_dir)
                print("Zip file extracted successfully")
            elif file_name.endswith('.tar.gz') or file_name.endswith('.tgz'):
                with tarfile.open(local_file_path, "r:gz") as tar:
                    tar.extractall(path=dataset_dir)
                print("Tar.gz file extracted successfully")
            else:
                print(f"Unsupported file format: {file_name}")
                return

            # Remove the compressed file after extraction
            os.remove(local_file_path)
            print(f"Removed the compressed file: {local_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading dataset from {dataset_url}: {e}")
        except (zipfile.BadZipFile, tarfile.TarError) as e:
            print(f"Error extracting dataset from {local_file_path}: {e}")

    def get_file_extension(self, content_type):
        content_type = content_type.lower()
        if 'zip' in content_type:
            return '.zip'
        elif 'gzip' in content_type or 'x-gzip' in content_type:
            return '.gz'
        elif 'tar' in content_type:
            return '.tar'
        elif 'octet-stream' in content_type:
            return ''  # Binary file, no specific extension
        else:
            return ''  # Unknown type, no extension


    def prepare_classification_dataset(self, dataset_dir):
        print("Preparing classification dataset...")

        # Locate the vehicle-c10-20 directory
        sub_dirs = [os.path.join(dataset_dir, d) for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
        if len(sub_dirs) != 1:
            raise ValueError("Expected a single subdirectory in the dataset directory")
        vehicle_dir = sub_dirs[0]
        print(f"Main Sub directory: {vehicle_dir}")

        images_dir = os.path.join(dataset_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        print(f"Images directory: {images_dir}")

        class_names = set()
        split_info = {}  # To keep track of which images belong to which split

        # Iterate through train, val, and test splits
        for split in ['train', 'val', 'test']:
            split_dir = os.path.join(vehicle_dir, split)
            dst_split_dir = os.path.join(images_dir, split)
            os.makedirs(dst_split_dir, exist_ok=True)
            split_info[split] = {}

            for class_name in os.listdir(split_dir):
                class_dir = os.path.join(split_dir, class_name)
                if os.path.isdir(class_dir):
                    class_names.add(class_name)
                    dst_class_dir = os.path.join(dst_split_dir, class_name)
                    os.makedirs(dst_class_dir, exist_ok=True)

                    # Copy images and keep track of which split they belong to
                    for img in os.listdir(class_dir):
                        src_path = os.path.join(class_dir, img)
                        dst_path = os.path.join(dst_class_dir, img)
                        shutil.copy2(src_path, dst_path)

                        if class_name not in split_info[split]:
                            split_info[split][class_name] = []
                        split_info[split][class_name].append(dst_path)

        # Retrieve class names and count
        self.num_classes = len(class_names)
        self.class_names = list(class_names)

        print(f"Number of classes: {self.num_classes}")
        print(f"Class names: {self.class_names}")

        # Optionally, you can save the split information for later use
        # For example, you could save it as a JSON file
        import json
        with open(os.path.join(dataset_dir, 'split_info.json'), 'w') as f:
            json.dump(split_info, f)



    

    def prepare_detection_dataset(self, dataset_dir):
        print("Preparing detection dataset...")

        # Find the downloaded folder
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [d for d in contents if os.path.isdir(os.path.join(dataset_dir, d))
                        and d not in ('images', 'annotations')]

        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return

        if len(downloaded_dirs) > 1:
            print(f"Multiple subdirectories found: {downloaded_dirs}. Using the first one.")

        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")

        # Source paths
        src_images_dir = os.path.join(downloaded_dir, 'images')
        src_annotations_dir = os.path.join(downloaded_dir, 'annotations')

        # Destination paths
        dst_images_dir = os.path.join(dataset_dir, 'images')
        dst_annotations_dir = os.path.join(dataset_dir, 'annotations')

        # Move images folder
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")

        # Move annotations folder
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(src_annotations_dir, dst_annotations_dir)
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")

        # Remove the downloaded folder if it's empty
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")

        print("Dataset preparation completed.")


    def convert_bbox_to_yolo(self, size, box):
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[2] / 2.0) * dw
        y = (box[1] + box[3] / 2.0) * dh
        w = box[2] * dw
        h = box[3] * dh
        return (x, y, w, h)

    def create_data_yaml(self, dataset_dir, class_names):
        data_yaml = {
            'path': dataset_dir,
            'train': 'images/train2017',
            'val': 'images/val2017',
            'test': 'images/test2017',
            'names': class_names
        }

        yaml_path = os.path.join(dataset_dir, 'data.yaml')
        with open(yaml_path, 'w') as file:
            yaml.dump(data_yaml, file, default_flow_style=False)

        print(f"Created data.yaml file at {yaml_path}")

    import os
    import shutil
    from pycocotools.coco import COCO

    def prepare_yolo_dataset(self, dataset_dir):
        print("Preparing YOLO dataset...")

        # Create the 'datasets' directory one level above the 'workspace' directory
        root_dir = os.path.abspath(os.path.join(dataset_dir, os.pardir, os.pardir))
        datasets_dir = os.path.join(root_dir, 'datasets')
        if not os.path.exists(datasets_dir):
            os.makedirs(datasets_dir)

        # New directory structure: datasets/workspace/dataset
        workspace_dir = os.path.basename(os.path.dirname(dataset_dir))
        new_workspace_dir = os.path.join(datasets_dir, workspace_dir)
        if not os.path.exists(new_workspace_dir):
            os.makedirs(new_workspace_dir)

        new_dataset_dir = os.path.join(new_workspace_dir, os.path.basename(dataset_dir))
        if os.path.exists(new_dataset_dir):
            shutil.rmtree(new_dataset_dir)
        shutil.move(dataset_dir, new_dataset_dir)
        dataset_dir = new_dataset_dir

        # Find the downloaded folder
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [d for d in contents if os.path.isdir(os.path.join(dataset_dir, d))
                           and d not in ('images', 'annotations')]

        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return

        if len(downloaded_dirs) > 1:
            print(f"Multiple subdirectories found: {downloaded_dirs}. Using the first one.")

        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")

        # Source paths
        src_images_dir = os.path.join(downloaded_dir, 'images')
        src_annotations_dir = os.path.join(downloaded_dir, 'annotations')

        # Destination paths
        dst_images_dir = os.path.join(dataset_dir, 'images')
        dst_annotations_dir = os.path.join(dataset_dir, 'annotations')

        # Move images folder
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")

        # Move annotations folder
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(src_annotations_dir, dst_annotations_dir)
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")

        # Convert annotations to YOLO format
        annotation_file = os.path.join(dst_annotations_dir, 'instances_train2017.json')
        coco = COCO(annotation_file)
        img_dir = dst_images_dir
        ann_dir = os.path.join(dataset_dir, 'labels')
        if not os.path.exists(ann_dir):
            os.makedirs(ann_dir)

        # Subdirectories for labels
        label_dirs = {
            'train': os.path.join(ann_dir, 'train2017'),
            'val': os.path.join(ann_dir, 'val2017'),
            'test': os.path.join(ann_dir, 'test2017')
        }
        for dir_path in label_dirs.values():
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        # Get class names
        categories = coco.loadCats(coco.getCatIds())
        class_names = [category['name'] for category in categories]

        for img_id in coco.getImgIds():
            img_info = coco.loadImgs(img_id)[0]
            img_filename = img_info['file_name']
            img_width = img_info['width']
            img_height = img_info['height']

            ann_ids = coco.getAnnIds(imgIds=img_id)
            anns = coco.loadAnns(ann_ids)

            if 'train' in img_filename:
                label_path = os.path.join(label_dirs['train'], img_filename.replace('.jpg', '.txt'))
            elif 'val' in img_filename:
                label_path = os.path.join(label_dirs['val'], img_filename.replace('.jpg', '.txt'))
            else:
                label_path = os.path.join(label_dirs['test'], img_filename.replace('.jpg', '.txt'))

            with open(label_path, 'w') as f:
                for ann in anns:
                    bbox = ann['bbox']
                    yolo_bbox = self.convert_bbox_to_yolo((img_width, img_height), bbox)
                    category_id = ann['category_id'] - 1
                    f.write(f"{category_id} {' '.join(map(str, yolo_bbox))}\n")

        # Remove the downloaded folder if it's empty
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")

        # Create the data.yaml file
        self.create_data_yaml(dataset_dir, class_names)

        print("Dataset preparation completed.")



    def get_checkpoint_path(self):
        try:
            checkpoint_dir = "./checkpoints"
            # Ensure the checkpoints directory exists
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
                print(f"Created checkpoint directory: {checkpoint_dir}")
                return None, False  # No checkpoints available
            # List all files in the checkpoints directory
            checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.endswith('.pt')]
            if not checkpoint_files:
                print("No checkpoint files found in the checkpoints directory.")
                return None, False
            # If there are multiple checkpoints, you might want to choose the most recent one
            # For simplicity, we're just choosing the first one here
            checkpoint_path = os.path.join(checkpoint_dir, checkpoint_files[0])
            print(f"Found checkpoint: {checkpoint_path}")
            return checkpoint_path, True
        except Exception as e:
            self.log_error(__file__, 'get_checkpoint_path', str(e))
            print(f"Exception in get_checkpoint_path: {str(e)}")
            return None, False

    def create_config(self):
        model_name = self.model_name
        action_type = self.action_type

        if action_type == 'train':
            config_path = os.path.join(os.getcwd(), 'configs', model_name, 'train-config.json')

            print(config_path)

            if os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    self.config = json.load(config_file)
                print(f"Loaded train config for model {model_name}: {self.config}")

                # Create model_config dictionary
                self.model_config = {}
                for config in self.config.get('actionConfig', []):
                    key_name = config.get('keyName')
                    default_value = config.get('defaultValue')
                    if key_name and default_value is not None:
                        self.model_config[key_name] = self.cast_value(config.get('valueType'), default_value)
                print(f"Model config: {self.model_config}")
            else:
                raise FileNotFoundError(f"Train configuration file not found for model {model_name} at {config_path}")

        elif action_type == 'export':
            config_dir = os.path.join(os.path.dirname(os.getcwd()), 'config', model_name)

            if os.path.exists(config_dir) and os.path.isdir(config_dir):
                self.export_configs = {}
                for file_name in os.listdir(config_dir):
                    if file_name.startswith('export-') and file_name.endswith('-config.json'):
                        export_format = file_name[len('export-'):-len('-config.json')]
                        export_config_path = os.path.join(config_dir, file_name)
                        with open(export_config_path, 'r') as config_file:
                            self.export_configs[export_format] = json.load(config_file)
                        print(f"Loaded export config for format {export_format}: {self.export_configs[export_format]}")
            else:
                raise FileNotFoundError(f"Export Configuration directory not found for model {model_name} at {config_dir}")
        else:
            raise ValueError(f"Unsupported action type: {action_type}")

    def cast_value(self, value_type, value):
        if value_type == "int32":
            return int(value)
        elif value_type == "float32":
            return float(value)
        elif value_type == "string":
            return str(value)
        elif value_type == 'bool':
            return bool(value)
        else:
            return value

    def update_status(self, stepCode, status, status_description):
        print(f"Mock update status: {stepCode}, {status}, {status_description}")

    def upload_checkpoint(self, checkpoint_path, model_type="trained"):
        print(f"Mock upload checkpoint: {checkpoint_path}, {model_type}")
        return True

    def download_model(self, model_path, model_type="trained"):
        print(f"Mock download model to: {model_path}, {model_type}")
        local_model_file = os.path.join(self.local_model_path, f"{model_type}_model.pth")
        with open(local_model_file, 'rb') as src, open(model_path, 'wb') as dest:
            dest.write(src.read())
        return True
    
    

    def get_job_params(self):
        # Return job params according to the requirements in train.py
        dataset_path = 'dataset'
        model_config = dotdict({
        'data': f"workspace/{dataset_path}/images",
        'val_ratio': 0.1,
        'test_ratio': 0.1,
        'batch_size': 1,
        'epochs': 1,
        'lr': 0.001,
        'momentum': 0.9,
        'weight_decay': 0.0001,
        'lr_step_size': 7,
        'lr_gamma': 0.1,
        'patience': 5,
        'min_delta': 0.001,
        'arch': self.model_arch,
        'pretrained': True,
        'gpu': 0,
        'dataset_path': dataset_path,
        'opt': 'adamw',
        'model_key':self.model_arch,
        'lr_scheduler': 'steplr',
        'checkpoint_path':self.checkpoint_path
    })

        return model_config

    def save_evaluation_results(self, list_of_result_dicts):
        print(f"Mock save evaluation results: {list_of_result_dicts}")

    def add_index_to_category(self, indexToCat):
        print(f"Mock add index to category: {indexToCat}")

    def get_index_to_category(self, is_exported=False):
        # Create a folder and save the data for the local run
        folder_path = os.path.join(self.local_model_path, "index_to_category")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "index_to_category.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            index_to_category = {}  # Example empty dictionary
            with open(file_path, 'w') as file:
                json.dump(index_to_category, file)
            return index_to_category

    def log_epoch_results(self, epoch, epoch_result_list):
        try:
            model_log_payload = {
                "_idModel": self._idModel,
                "epoch": epoch,
                "epochDetails": epoch_result_list,
            }

            print(model_log_payload)

        except Exception as e:
            self.log_error(__file__, 'log_epoch_results', str(e))
            print(f"Exception in log_epoch_results: {str(e)}")
            self.update_status("error", "error", "Failed to log epoch results")
            sys.exit(1)

    def get_metrics(data_loader, model , device, index_to_labels):

        all_outputs = []
        all_targets = []

        print(model)
        print(device)
        print(index_to_labels)

        # Set model to evaluation mode for inference
        model.eval()
        print("Model evaluating")

        # Accumulate predictions (detcetion)
        # with torch.no_grad():
        #     for images, targets in data_loader:
        #         images = [image.to(device) for image in images]
        #         targets = [{k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in t.items()} for t in targets]

        #         outputs = model(images)
        #         all_outputs.extend(outputs)
        #         all_targets.extend(targets)

        print("Model evaluated")
