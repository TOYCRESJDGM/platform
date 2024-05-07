CREATE TABLE emitters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_number VARCHAR(255) NOT NULL,
    name VARCHAR(150) NOT NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modification_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (document_number)
);


CREATE TABLE receivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_number VARCHAR(255) NOT NULL,
    name VARCHAR(150) NOT NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modification_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (document_number)
);


CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number_invoice VARCHAR(255) NOT NULL,
    date_issued DATE NOT NULL,
    pdf_url VARCHAR(255),
    emitter_id INT,
    receiver_id INT,
    series VARCHAR(10),
    folio INT,
    tax INT,
    total INT,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modification_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (emitter_id) REFERENCES emitters(id),
    FOREIGN KEY (receiver_id) REFERENCES receivers(id)
);


CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    code VARCHAR(255) NOT NULL,
    description TEXT,
    date_event DATETIME NOT NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modification_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES invoice(id)
);
