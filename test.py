INSERT INTO Instructor(ins_ID, lastname, firstname, city, country)
VALUES("id7", "Cqldano", "Antonio", "Vancouver", "Canada");

INSERT INTO Instructor(ins_ID, lastname, firstname, city, country)
VALUES("id8", "Ryan", "Steve", "Vancouver", "Canada")
(9, km)

UPDATE Instructor
SET city=Markham
WHERE ins_id=1;

UPDATE Instructor
SET city="Dhaka", country="BD"
WHERE ins_id=4;

DELETE FROM Instructor
WHERE firstname="Hima";