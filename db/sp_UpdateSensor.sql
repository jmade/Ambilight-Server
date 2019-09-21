/*
sp_UpdateSensor
Created: JDM
Date:  2019-7-30
Descr: Updates Pulled to 1 and updated the records updatedAt TimeStamp
*/

drop procedure if exists sp_UpdateSensor;

delimiter //

create procedure sp_UpdateSensor(
	in pId Int
)

begin

UPDATE video
SET 
	downloaded = 1,
	downloadDate = CURRENT_TIMESTAMP()
WHERE 
	id = pId
;

end;
//

delimiter ;