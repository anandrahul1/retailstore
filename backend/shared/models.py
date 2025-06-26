from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Base Models
class BaseEntity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# User Models
class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(BaseEntity):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.CUSTOMER
    is_active: bool = True
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Product Models
class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"

class Product(BaseEntity):
    name: str
    description: str
    price: float
    category: ProductCategory
    sku: str
    stock_quantity: int
    images: List[str] = []
    attributes: Dict[str, Any] = {}
    is_active: bool = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: ProductCategory
    sku: str
    stock_quantity: int
    images: List[str] = []
    attributes: Dict[str, Any] = {}

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[ProductCategory] = None
    stock_quantity: Optional[int] = None
    images: Optional[List[str]] = None
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

# Cart Models
class CartItem(BaseModel):
    product_id: str
    quantity: int
    price: float
    product_name: str

class Cart(BaseEntity):
    user_id: str
    items: List[CartItem] = []
    total_amount: float = 0.0

class CartItemAdd(BaseModel):
    product_id: str
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

# Order Models
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float
    total: float

class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class Order(BaseEntity):
    user_id: str
    order_number: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.PENDING
    shipping_address: ShippingAddress
    payment_method: str
    notes: Optional[str] = None

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: str
    notes: Optional[str] = None

# Event Models
class EventType(str, Enum):
    USER_REGISTERED = "user.registered"
    ORDER_CREATED = "order.created"
    ORDER_CONFIRMED = "order.confirmed"
    ORDER_SHIPPED = "order.shipped"
    ORDER_DELIVERED = "order.delivered"
    PAYMENT_COMPLETED = "payment.completed"
    INVENTORY_LOW = "inventory.low"

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    source: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None

# Response Models
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

# Token Models
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None