--read procedure
--retrieves trail using id
CREATE PROCEDURE CW1.ReadTrail
@TrailID INT
AS
BEGIN

    SELECT * FROM CW1.Trail
    WHERE TrailID = @TrailID;
END;
