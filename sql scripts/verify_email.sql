
CREATE TABLE `verify_email` (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
`email` TEXT NOT NULL ,
`hash` VARCHAR( 32 ) NOT NULL ,
`active` VARCHAR( 1 ) NOT NULL DEFAULT 'N'
)