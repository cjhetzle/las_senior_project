from src.Database import Database

class DatabaseTest:

  def __init__(self):
    pass

  def main(self):
    self.load_data_test(self)
    self.save_data_test(self)

  def load_data_test(self):
    pass

  def save_data_test(self):
    db = Database("test.txt");
    Database.save_data();

