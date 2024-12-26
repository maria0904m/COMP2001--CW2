CREATE PROCEDURE [CW2].[InsertTrail]
    @Name VARCHAR(100),
    @Length DECIMAL(5,2),
    @Elevation INT,
    @Type VARCHAR(50),
    @Difficulty VARCHAR(50),
    @Description VARCHAR(255),
    @CountryID INT
AS
BEGIN 
    INSERT INTO CW2.Trail (Name, Length, Elevation, Type, Difficulty, Description, CountryID)
    VALUES (@Name, @Length, @Elevation, @Type, @Difficulty, @Description, @CountryID);
END;