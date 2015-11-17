import importlib
import sys
import csv
import datetime
import math

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
GYM_NAME = "network_intrusion_detection"  # or use "rec-center-every-15m-large"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"

DATE_FORMAT = "%m/%d/%y %H:%M"


def createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "class"})
  return model

def getModelParamsFromName(gymName):
 # importName = "model_params.%s_model_params" % (MODEL_PARAMS_DIR, gymName.replace(" ", "_").replace("-", "_"))
  importName = "network_intrusion_detection_model_params"
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % gymName)
  return importedModelParams


def runIoThroughNupic(inputData, model, gymName, plot):
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  
  counter = 0
  for row in csvReader:
    counter += 1
    #timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    duration = int(row[0])
    # print duration
    protocol_type = str(row[1])
    # print protocol_type
    service = str(row[2])
    # print service
    flag = str(row[3])
    # print flag
    src_bytes = int(row[4])
    # print src_bytes
    dst_bytes = int(row[5])
    # print dst_bytes
    classs = str(row[6])
    # print classs
    result = model.run({
      "duration": duration,
      "protocol_type": protocol_type,
      "service": service,
      "flag": flag,
      "src_bytes": src_bytes,
      "dst_bytes": dst_bytes,
      "class": classs
    })

    # prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    print anomalyScore
    #print prediction

  inputFile.close()

def runModel(gymName, plot=False):
  print "Creating model from %s..." % gymName
  model = createModel(getModelParamsFromName(gymName))
  inputData = "%s/%s.csv" % (DATA_DIR, gymName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, gymName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(GYM_NAME, plot=plot)
