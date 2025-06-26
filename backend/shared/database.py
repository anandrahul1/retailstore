import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import os

class DynamoDBClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.region_name = region_name
    
    def get_table(self, table_name: str):
        return self.dynamodb.Table(table_name)
    
    async def create_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item in DynamoDB table"""
        try:
            table = self.get_table(table_name)
            
            # Add timestamps
            now = datetime.utcnow().isoformat()
            item['created_at'] = now
            item['updated_at'] = now
            
            table.put_item(Item=item)
            return item
        except ClientError as e:
            raise Exception(f"Error creating item: {e.response['Error']['Message']}")
    
    async def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get an item by primary key"""
        try:
            table = self.get_table(table_name)
            response = table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            raise Exception(f"Error getting item: {e.response['Error']['Message']}")
    
    async def update_item(self, table_name: str, key: Dict[str, Any], 
                         update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing item"""
        try:
            table = self.get_table(table_name)
            
            # Build update expression
            update_expression = "SET updated_at = :updated_at"
            expression_values = {":updated_at": datetime.utcnow().isoformat()}
            
            for field, value in update_data.items():
                if field not in ['id', 'created_at']:
                    update_expression += f", {field} = :{field}"
                    expression_values[f":{field}"] = value
            
            response = table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            return response['Attributes']
        except ClientError as e:
            raise Exception(f"Error updating item: {e.response['Error']['Message']}")
    
    async def delete_item(self, table_name: str, key: Dict[str, Any]) -> bool:
        """Delete an item"""
        try:
            table = self.get_table(table_name)
            table.delete_item(Key=key)
            return True
        except ClientError as e:
            raise Exception(f"Error deleting item: {e.response['Error']['Message']}")
    
    async def query_items(self, table_name: str, key_condition: Any, 
                         filter_condition: Any = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Query items with key condition"""
        try:
            table = self.get_table(table_name)
            
            kwargs = {
                'KeyConditionExpression': key_condition,
                'Limit': limit
            }
            
            if filter_condition:
                kwargs['FilterExpression'] = filter_condition
            
            response = table.query(**kwargs)
            return response['Items']
        except ClientError as e:
            raise Exception(f"Error querying items: {e.response['Error']['Message']}")
    
    async def scan_items(self, table_name: str, filter_condition: Any = None, 
                        limit: int = 100) -> List[Dict[str, Any]]:
        """Scan table with optional filter"""
        try:
            table = self.get_table(table_name)
            
            kwargs = {'Limit': limit}
            if filter_condition:
                kwargs['FilterExpression'] = filter_condition
            
            response = table.scan(**kwargs)
            return response['Items']
        except ClientError as e:
            raise Exception(f"Error scanning items: {e.response['Error']['Message']}")

# Database configuration
class DatabaseConfig:
    USERS_TABLE = os.getenv("USERS_TABLE", "retail-users")
    PRODUCTS_TABLE = os.getenv("PRODUCTS_TABLE", "retail-products")
    CARTS_TABLE = os.getenv("CARTS_TABLE", "retail-carts")
    ORDERS_TABLE = os.getenv("ORDERS_TABLE", "retail-orders")
    
    @classmethod
    def get_table_name(cls, service: str) -> str:
        table_mapping = {
            "users": cls.USERS_TABLE,
            "products": cls.PRODUCTS_TABLE,
            "carts": cls.CARTS_TABLE,
            "orders": cls.ORDERS_TABLE
        }
        return table_mapping.get(service, f"retail-{service}")

# Global database client
db_client = DynamoDBClient()