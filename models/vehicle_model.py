from db_config.mysql import MysqlDB

class Vehicle():
  db_instance = None

  def __init__(self,):
    if self.db_instance is None:
      self.db_instance = MysqlDB.get_instance()
  
  # Funcion que hace la busqueda de la placa en la BD
  def find_vehicle(self, plate_number):
    try:
      connection = self.db_instance.get_connection()
      if connection is not None and connection.is_connected():
        cursor = connection.cursor(dictionary=True)
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
        if not result:
          return (False, None)
        return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      if 'cursor' in locals() and cursor is not None:
            cursor.close()
      if 'connection' in locals() and connection.is_connected():
          connection.close()

  def load_access_type(self):
    try:
      connection = self.db_instance.get_connection()
      if connection is not None and connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * from access_type
              """
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
          return {"loaded": False }
        return {"loaded": False, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      if 'cursor' in locals() and cursor is not None:
            cursor.close()
      if 'connection' in locals() and connection.is_connected():
          connection.close()

  def load_status_type(self):
    try:
      connection = self.db_instance.get_connection()
      if connection is not None and connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * from status_type
              """
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
          {"loaded": False }
        return {"loaded": False, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      if 'cursor' in locals() and cursor is not None:
            cursor.close()
      if 'connection' in locals() and connection.is_connected():
          connection.close()

  def load_vehicles_type(self):
    try:
      connection = self.db_instance.get_connection()
      if connection is not None and connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * from vehicles_type
              """
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
          {"loaded": False }
        return {"loaded": False, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      if 'cursor' in locals() and cursor is not None:
            cursor.close()
      if 'connection' in locals() and connection.is_connected():
          connection.close()
  
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