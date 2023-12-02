from db_config.mysql import conn
from db_constants.common_functions import closeConnection, openConnection

class Vehicle():
  conn = None
  cursor = None
  def __init__(self,):
    self.conn = conn
  
  def new_cursor(self):
    return self.conn.cursor(dictionary=True)
  
  # Funcion que hace la busqueda de la placa en la BD
  def find_vehicle(self, plate_number):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT 
            vehicles.id AS id, 
            plate_number,
            status_type_id,
            access_type_id,
            vehicles_type.id AS vehicle_type_id
          FROM vehicles
          INNER JOIN vehicles_type
          ON vehicles_type.id = vehicles.vehicle_type_id
          INNER JOIN status_type
          ON status_type.id = vehicles.status_type_id
          INNER JOIN access_type
          ON access_type.id = vehicles.access_type_id
          WHERE vehicles.plate_number=%s"""
      params = (plate_number,)
      cursor.execute(query, params)
      result = cursor.fetchone()
      if result == None:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      cursor.close()

  def load_access_type(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * from access_type
            """
      cursor.execute(query)
      result = cursor.fetchall()
      if result == None:
        return {"loaded": False }
      return {"loaded": False, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      cursor.close()

  def load_status_type(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * from status_type
            """
      cursor.execute(query)
      result = cursor.fetchall()
      if result == None:
        {"loaded": False }
      return {"loaded": False, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      cursor.close()

  def load_vehicles_type(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * from vehicles_type
            """
      cursor.execute(query)
      result = cursor.fetchall()
      if result == None:
        {"loaded": False }
      return {"loaded": False, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      cursor.close()
  
  def load_required_data(self):
    try:
      access_type = self.load_access_type()
      status_type = self.load_status_type()
      vehicles_type = self.load_vehicles_type()
      data = {
        "vehicles_type": (),
        "status_type": (),
        "access_type": ()
      } 
      if access_type["loaded"]:
        data["access_type"] = access_type["data"]
      
      if status_type["loaded"]:
        data["status_type"] = status_type["data"]

      if vehicles_type["loaded"]:
        data["vehicles_type"] = vehicles_type["data"]

      return (True, data)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
 
VehicleModel = Vehicle()