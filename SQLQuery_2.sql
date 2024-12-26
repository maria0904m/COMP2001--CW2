CREATE PROCEDURE CW2.UpdateTrail
    @TrailID INT,
    @Name VARCHAR(255),
    @Description TEXT,
    @CountryID INT  
AS
BEGIN
    UPDATE CW2.Trail
    SET Name = @Name,
        Description = @Description,
        CountryID = @CountryID
    WHERE TrailID = @TrailID;
END;