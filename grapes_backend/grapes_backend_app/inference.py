import numpy as np
import os, cv2, json, shapely
import base64
import datetime

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import ColorMode
setup_logger()

# DATASET AND METADATA
def _get_grapes_dict(name: str, set_name: str):
  json_file = "./grapes_backend_app/annotations/" + name
  with open(json_file) as f:
    imgs_anns = json.load(f)

  dataset_dicts = []
  for image in imgs_anns["images"]:
    record = {}
    record["file_name"] = os.path.join(
      "./grapes_backend_app/images/multiple-instance-multiple-class/" + set_name,
      image["file_name"])
    record["image_id"] = image["id"]
    record["height"] = image["height"]
    record["width"] = image["width"]

    annotations = [a for a in imgs_anns["annotations"] if a.get('image_id') == record["image_id"]]
    for annot in annotations:
      annot["category_id"] = annot["category_id"]
      annot["bbox_mode"] = 1
      bbox = tuple(annot["bbox"])
      polygon = shapely.geometry.box(*(bbox[0],bbox[1],bbox[0]+bbox[2], bbox[1]+bbox[3]), ccw=True)
      K = str(polygon.wkt).split("POLYGON ((")[-1].split("))")[0].split(',')
      polygon=[]
      for m in K:
        for p in m.split(" "):
          if p:
            polygon.append(int(p))

      polygon=[polygon]
      annot["segmentation"] = polygon

    record["annotations"] = annotations

    dataset_dicts.append(record)

  return dataset_dicts


def _get_all_dicts():
  train =  _get_grapes_dict("mimc_train_images.json", "train_set")
  return {
    "train": train
  }


def _register_datasets():
  dicts = _get_all_dicts()
  DatasetCatalog.clear()
  for key in ["train"]:#"test", "valid"]:
    DatasetCatalog.register("grapes_" + key, lambda d = dicts: d[key])
    MetadataCatalog.get("grapes_" + key).set(
      thing_classes=["Immature", "Semi Mature", "Mature"],
      thing_dataset_id_to_contiguous_id = {0: 1, 1: 2, 2: 3})


_register_datasets()
grapes_metadata = MetadataCatalog.get("grapes_train")


# SETUP
cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"
cfg.merge_from_file("./detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3
cfg.OUTPUT_DIR = "./grapes_backend_app/output"
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.77
predictor = DefaultPredictor(cfg)


# FUNCTIONS
def predict(image_bin, ph = 0.00):
  im = cv2.imdecode(np.fromstring(image_bin.read(), np.uint8), cv2.IMREAD_UNCHANGED)
  im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
  outputs = predictor(im)
  
  v = Visualizer(im[:, :, ::-1],
    metadata = grapes_metadata
  )

  out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
  img_b64 = base64.b64encode(
    cv2.imencode('.jpg', out.get_image()[:, :, ::-1])[1]
  ).decode('utf-8')

  return {
    "date_time": str(datetime.datetime.now()),
    "annotated_image": img_b64,
    "overall_maturity": _get_overall_maturity(outputs["instances"], float(ph)),
    "ph": ph
  }

# ph: 3.1 o menos -> inmaduras
#     3.4 - 3.8 o mas -> maduras
def _get_overall_maturity(instances, ph = 0.00):
  overall_maturity = 0.00
  count = 0

  if ph < 3:
    ph = 3.00
  elif ph > 4.00:
    ph = 4.00

  ph_norm = (ph - 3.00) / (4.00 - 3.00)
  ph_maturity = ph_norm * 2

  for number in instances.pred_classes:
    overall_maturity += (number + ph_maturity)
    count += 2

  try:
    maturity_num = float(overall_maturity / count)
  except ZeroDivisionError:
    return "None"
  except:
    return "None"
  
  return grapes_metadata.thing_classes[round(maturity_num)]
  