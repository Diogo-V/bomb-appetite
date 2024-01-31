CREATE DATABASE IF NOT EXISTS db;
use db;

-- Create tables

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE restaurant (
    id VARCHAR(36) PRIMARY KEY,
    owner VARCHAR(100) NOT NULL,
    restaurant VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    genre TEXT
);

CREATE TABLE menuitem (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    currency VARCHAR(100) NOT NULL,

    restaurant_id VARCHAR(36),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
);

CREATE TABLE voucher (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    restaurant_id VARCHAR(36) NOT NULL,
    user_id INTEGER NOT NULL,
    code VARCHAR(100) NOT NULL,
    discount NUMERIC(10,2) NOT NULL,
    description VARCHAR(100) NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id VARCHAR(36) NOT NULL,
    review TEXT NOT NULL,
    rating INTEGER NOT NULL,
    signature VARCHAR(255) NOT NULL,

    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);


-- Populate with some data

INSERT INTO user (id, name) VALUES ('1', 'John Doe');
INSERT INTO user (id, name) VALUES ('2', 'Jane Doe');
INSERT INTO user (id, name) VALUES ('3', 'John Smith');
INSERT INTO user (id, name) VALUES ('4', 'Jane Smith');
INSERT INTO user (id, name) VALUES ('5', 'John Doe Jr');

INSERT INTO restaurant (id, owner, restaurant, address, genre) VALUES ('1', 'John Doe', 'Papa John', '123 Main St, New York, NY 10001', 'Pizza');
INSERT INTO restaurant (id, owner, restaurant, address, genre) VALUES ('2', 'Jane Doe', 'McDonalds', '456 Main St, New York, NY 10001', 'Fast Food,Burgers');
INSERT INTO restaurant (id, owner, restaurant, address, genre) VALUES ('3', 'John Doe', 'Burger King', '789 Main St, New York, NY 10001', 'Fast Food');
INSERT INTO restaurant (id, owner, restaurant, address, genre) VALUES ('4', 'Jane Doe', 'Taco Bell', '101 Main St, New York, NY 10001', 'Mexican');
INSERT INTO restaurant (id, owner, restaurant, address, genre) VALUES ('5', 'John Doe', 'Subway', '112 Main St, New York, NY 10001', 'Sandwiches');
INSERT INTO restaurant (id, owner, restaurant, address, genre) VALUES ('6', 'Jane Doe', 'Wendys', '131 Main St, New York, NY 10001', 'Fast Food,Burgers');

INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('1', 'Cheese Pizza', 'Pizza', 'Cheese Pizza', 10.00, 'USD', '1');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('2', 'Pepperoni Pizza', 'Pizza', 'Pepperoni Pizza', 12.00, 'USD', '1');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('3', 'Hamburger', 'Burgers', 'Hamburger', 5.00, 'USD', '2');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('4', 'Cheeseburger', 'Burgers', 'Cheeseburger', 6.00, 'USD', '2');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('5', 'Chicken Sandwich', 'Sandwiches', 'Chicken Sandwich', 5.00, 'USD', '5');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('6', 'Steak Sandwich', 'Sandwiches', 'Steak Sandwich', 6.00, 'USD', '5');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('7', 'Taco', 'Tacos', 'Taco', 3.00, 'USD', '4');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('8', 'Burrito', 'Burritos', 'Burrito', 5.00, 'USD', '4');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('9', 'Chicken Nuggets', 'Chicken', 'Chicken Nuggets', 5.00, 'USD', '3');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('10', 'Chicken Sandwich', 'Sandwiches', 'Chicken Sandwich', 5.00, 'USD', '3');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('11', 'Hamburger', 'Burgers', 'Hamburger', 5.00, 'USD', '6');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('12', 'Cheeseburger', 'Burgers', 'Cheeseburger', 6.00, 'USD', '6');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('13', 'Chicken Sandwich', 'Sandwiches', 'Chicken Sandwich', 5.00, 'USD', '6');
INSERT INTO menuitem (id, name, category, description, price, currency, restaurant_id) VALUES ('14', 'Steak Sandwich', 'Sandwiches', 'Steak Sandwich', 6.00, 'USD', '6');

INSERT INTO voucher (id, restaurant_id, user_id, code, discount, description, is_deleted) VALUES ('1', '1', '1', '10OFF', 10.00, '10% off your order', 0);
INSERT INTO voucher (id, restaurant_id, user_id, code, discount, description, is_deleted) VALUES ('2', '2', '2', '20OFF', 20.00, '20% off your order', 0);
INSERT INTO voucher (id, restaurant_id, user_id, code, discount, description, is_deleted) VALUES ('3', '3', '2', '30OFF', 30.00, '30% off your order', 0);
INSERT INTO voucher (id, restaurant_id, user_id, code, discount, description, is_deleted) VALUES ('4', '4', '3', '15OFF', 15.00, '15% off your order', 0);
