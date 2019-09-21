drop procedure if exists sp_GetSensorReadings;

delimiter //

create procedure sp_GetSensorReadings(
    in pRoom varchar(32)
)

begin
main: begin

declare vSensorId int;
declare vCharacteristicid int;

declare vRoomId int;

set vRoomId to select id from Room where name = pRoom;
-- select id from Sensor where room_id = vRoomId as SensorId;
select * from vRoomId;

create temporary table tmpRestrict as
select EqId
from RestrictHeroEq
where HeroId = pAppHeroId;


create temporary table tmpTab (
	Id bigint
) engine = memory;  # Rev4.1.0a

insert into tmpTab (
		CustId




-- CREATE TEMPORARY TABLE TMP(
    
-- );

-- select * from TMP;

-- create TEMPORARY TABLE results (
--    id int,
--    char_id int
-- );

-- -- into (vSensorId,vCharacteristicid)
-- -- (`id`,`characteristic_id`)

-- select id from Sensor 
--   where room_id=(
--     select id from Room where name = pRoom
--   )
-- );

end main;
end;
//

delimiter ;