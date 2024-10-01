from neospaceai.manager import Manager

class Neospace:
  def __init__(self, report_name):
    self.manager = Manager()
    self.report_name = report_name

  def getModelFromLastExecution(self, cycle_name: str, epoch: int) -> str:
    data = self.manager.getCycles(cycle_name)

    if data:
      for execution in data:
        if execution.get('status') == "SUCCEEDED":
          job = execution.get('jobs')[cycle_name]
          num_epochs = job['hyperparameters']['epochs']
          if num_epochs < 1 or num_epochs < epoch:
            print(f"No execution found for epoch {epoch}")
            break

          epoch = job['epochs'][epoch-1]
          if epoch.get('modelId'):
            model = self.manager.getModelById(epoch['modelId'])
            return model['path']
          else:
            print(f"No model found for epoch {epoch}")
            return None 
    else:
      print("No data received from getCycles")
      return None