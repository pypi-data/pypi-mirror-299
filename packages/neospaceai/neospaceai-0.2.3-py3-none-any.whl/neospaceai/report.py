import os
from neospaceai.manager import Manager

class Model:
  num_epochs: int
  epoch: int
  path: str


class Neospace:
  def __init__(self, report_name=""):
    self.dir = os.path.expanduser("~/neospace-reports")
    self.manager = Manager()
    self.report_name = report_name
  
  def getReportDir(self):
    return self.dir
  
  def saveReport(self, filename: str, content: any):
    dirname = f'{self.dir}/{self.report_name}'
    if not os.path.exists(dirname):
      os.makedirs(dirname)
    filepath = os.path.join(dirname, filename)
    # Append content to the file (creates it if it doesn't exist)
    with open(filepath, 'a') as file:
      file.write(str(content) + '\n')


  def getModelFromLastExecution(self, cycle_name: str, epoch: int) -> Model:
    data = self.manager.getCycles(cycle_name)

    if data:
      for execution in data:
        if execution.get('status') == "SUCCEEDED":
          job = execution.get('jobs')[cycle_name]
          num_epochs = job['hyperparameters']['epochs']
          if num_epochs < 1 or num_epochs < epoch:
            print(f"No execution found for epoch {epoch}")
            break

          model = job['epochs'][epoch-1]
          if model.get('modelId'):
            model_response = self.manager.getModelById(model['modelId'])
            model = Model()
            model.num_epochs = num_epochs
            model.epoch = epoch
            model.path = model_response['path']
            return model
          else:
            print(f"No model found for epoch {epoch}")
            return None  
    else:
      print("No data received from getCycles")
      return None