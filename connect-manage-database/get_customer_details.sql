SELECT customer.lname,
          customer.fname,
          address.city,
          address.code
FROM   T_CUSTOMERS AS customer 
          LEFT JOIN T_ADDRESSES AS address ON address.id = customer.id 
WHERE  customer.lname = 'Trujillo'