CREATE PROCEDURE CW2.InsertTrail
    @Name VARCHAR(255),
    @Description TEXT,
    @CountryID INT,  
    @Length FLOAT 
AS
BEGIN
    INSERT INTO CW2.Trail (Name, Description, CountryID, Length)
    VALUES (@Name, @Description, @CountryID, @Length); 
END;
