CREATE PROCEDURE [CW2].[DeleteTrail]
    @TrailID INT
AS
BEGIN
    DELETE FROM CW2.Trail
    WHERE TrailID = @TrailID;
END;
