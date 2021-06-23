from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import pprint

class AnimalShelter(object):
    #CRUD operations for Animal collection in MongoDB
    
    def __init__(self, user:str , passw:str): 
        """Initialize MongoClient for MongoDB access
           Class expects a username and password as strings"""

        self.client = MongoClient('mongodb://%s:%s@localhost:43005/AAC' % (user, passw))
        self.database = self.client['AAC']
        
    def create(self, data: dict, path: bool):
        """Function to insert data into MongoDB
           Takes a dictionary and boolean as arguments
           Dictionary is the data to be inserted into the db
           Boolean is to verify if it's insert_one or insert_many
           insert_one = True, insert_many = False"""
        
        #check if passed in dictionary is empty
        if data is not None:
            
            if path is True: #Take insert_one path

                result = self.database.animals.insert_one(data) #insert single document

                if result.acknowledged: #if the insert happened correctly
                    print("True")

                else: #something went wrong with insert
                    print("False")
                
            elif path is False: #Take insert_many path

                result = self.database.animals.insert_many(data) #insert many documents

                if result.acknowledged: #if the insert happened correctly
                    print("True")

                else: #something went wrong with insert
                    print("False")

        else: #Passed in data is empty
            raise Exception('Nothing to save, data parameter is empty')
            return False
        
    def read(self, object_id: dict):
        """Function to read specific document from MongoDB
           Takes a specific ObjectId as a dictionary to call the document"""
        
        #Check if passed in dictionary is empty
        if object_id is not None:

            result = self.database.animals.find(object_id) #find object based on dictionary query

            if result is None: #Could not find query since return is of length 0
                print('Query does not exist')
                return

            return result
            
        else: #Passed in dictionary is empty
            raise Exception('ObjectId cannot be null')
            
    def read_no_id(self, object_id: dict):
        """Function to read specific document from MongoDB
            Excludes the bson _id tag
            Expects a specific objectId as a dictionary to call the document"""
        
        #Check if passed in dictionary is empty
        if object_id is not None:
            
            result = self.database.animals.find(object_id, {"_id": 0, "1": 0})
            
            if result is None: #Could not find query since return is of length 0
                print('Query does not exist')
                return
            
            return result
        
        else: #Passed in dictionary is empty
            raise Exception('ObjectId cannot be null')
        
    def update(self, lookup: dict, update_data: dict, path: bool):
        """Function to update a specific document in MongoDB
           Update takes three parameters: A dictionary to look up the document (lookup),
           The data to update on said document (update_data)
           The path if the desire is to update_one or update_many (path)"""

        #Check if lookup dict is empty
        if lookup is not None:

            if path is True: #Takes the update_one path

                result = self.database.animals.update_one(lookup, {"$set": update_data}) #Update first document which makes lookup dict

                if result.modified_count > 0: #Checks if a document has been updated
                    print("Update Results:\n" + dumps(result.raw_result, indent=2)) #print results

                else: #No document was updated
                    print("Invalid update query or nothing to update")

            elif path is False: #Takes the update_many path

                result = self.database.animals.update_many(lookup, {"$set": update_data}) #Update all documents which match the lookup dict

                if result.modified_count > 0: #Checks if any documents have been updated
                    print("Update Results:\n" + dumps(result.raw_result, indent=2)) #print results

                else: #No document was updated
                    print("Invalid update query or nothing to update")
        
        #Lookup dict is empty        
        else:
            raise Exception('Lookup criteria cannot be null')
            
    def delete(self, lookup: dict, path: bool):
        """Function to delete a specific document in MongoDB
           Update takes two parameters: A dictionary to look up the document (lookup),
           The path if the desire is to delete_one or delete_many (path)"""

        #Check if lookup dict is empty
        if lookup is not None:

            if path is True: #Takes the delete_one path
                result = self.database.animals.delete_one(lookup) #Delete first document which matches lookup dict

                if result.deleted_count > 0: #Checks if document was deleted
                    print("Delete Results:\n" + dumps(result.raw_result, indent=2)) #print results

                else: #Document was not deleted
                    print("Invalid delete query or nothing to delete")
                
            elif path is False: #Takes the delete_many path
                result = self.database.animals.delete_many(lookup) #Delete all documents which match lookup dict

                if result.deleted_count > 0: #Check if documents were deleted 
                    print("Delete Results:\n" + dumps(result.raw_result, indent=2)) #print results

                else: #Documents were not deleted
                    print("Invalid delete query or nothing to delete")
        
        #Lookup dict is empty        
        else:
            raise Exception('Lookup criteria cannot be null')
#            
#def main():
    #test = AnimalShelter('aacuser', 'AACUSERLOGIN')
    #result = test.read({'animal_type':'Dog', 'name':'Lucy'})
    #print(result)
    
#if __name__ == "__main__":
    #main()
