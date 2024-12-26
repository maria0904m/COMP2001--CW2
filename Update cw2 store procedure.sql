CREATE PROCEDURE [CW2].[UpdateTrail]
    @TrailID INT,
    @Name VARCHAR(100),
    @Length DECIMAL(5,2),
    @Elevation INT,
    @Type VARCHAR(50),
    @Difficulty VARCHAR(50),
    @Description VARCHAR(255),
    @CountryID INT
AS
BEGIN 
    UPDATE CW2.Trail
    SET Name = @Name, 
        Length = @Length, 
        Elevation = @Elevation, 
        Type = @Type,
        Difficulty = @Difficulty, 
        Description = @Description, 
        CountryID = @CountryID
    WHERE TrailID = @TrailID;
END;
