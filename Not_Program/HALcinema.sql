CREATE DATABASE HALcinema;
use HALcinema;

CREATE TABLE `Account` (
  `AccountID` int PRIMARY KEY AUTO_INCREMENT,
  `AccountNumber` varchar(8),
  `Name` varchar(50),
  `KanaName` varchar(50),
  `SexID` int,
  `Password` varchar(12),
  `MailAddress` varchar(255),
  `PhoneNumber` varchar(13),
  `Birthday` date,
  `MemberFlg` bit(1) DEFAULT 0,
  `RegistDate` datetime DEFAULT (now())
);

CREATE TABLE `Address` (
  `AddressID` int PRIMARY KEY AUTO_INCREMENT,
  `PostNumber` varchar(8),
  `Todohuken` varchar(8),
  `ShiKu` varchar(20),
  `ChoSonNumber` varchar(255),
  `AccountID` int
);

CREATE TABLE `Sex` (
  `SexID` int PRIMARY KEY AUTO_INCREMENT,
  `Sex` varchar(4)
);

CREATE TABLE `Movie` (
  `MovieID` int PRIMARY KEY AUTO_INCREMENT,
  `Movie` varchar(50),
  `MovieThum` varchar(100),
  `AgeLimitID` int DEFAULT 1,
  `MD` varchar(50),
  `MS` varchar(50),
  `Overview` varchar(2000),
  `StartDate` date,
  `FinishDate` date
);

CREATE TABLE `Screen` (
  `ScreenID` int PRIMARY KEY AUTO_INCREMENT,
  `Capacity` int
);

CREATE TABLE `Showing` (
  `ShowingID` int PRIMARY KEY AUTO_INCREMENT,
  `ShowDatetime` datetime,
  `MovieID` int,
  `ScreenID` int
);

CREATE TABLE `Price` (
  `PriceID` int PRIMARY KEY AUTO_INCREMENT,
  `PricingPlans` varchar(20),
  `Price` int
);

CREATE TABLE `Discount` (
  `DiscountID` int PRIMARY KEY AUTO_INCREMENT,
  `DiscountName` varchar(30),
  `Discount` float
);

CREATE TABLE `Reservation` (
  `ReservationID` int PRIMARY KEY AUTO_INCREMENT,
  `AccountID` int,
  `ShowingID` int,
  `SeatNumber` varchar(3),
  `PriceID` int,
  `DiscountID` int
);

CREATE TABLE `AgeLimit` (
  `AgeLimitID` int PRIMARY KEY AUTO_INCREMENT,
  `AgeLimit` varchar(5)
);

ALTER TABLE `Account` ADD FOREIGN KEY (`SexID`) REFERENCES `Sex` (`SexID`);

ALTER TABLE `Address` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Movie` ADD FOREIGN KEY (`AgeLimitID`) REFERENCES `AgeLimit` (`AgeLimitID`);

ALTER TABLE `Showing` ADD FOREIGN KEY (`MovieID`) REFERENCES `Movie` (`MovieID`);

ALTER TABLE `Showing` ADD FOREIGN KEY (`ScreenID`) REFERENCES `Screen` (`ScreenID`);

ALTER TABLE `Reservation` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Reservation` ADD FOREIGN KEY (`ShowingID`) REFERENCES `Showing` (`ShowingID`);

ALTER TABLE `Reservation` ADD FOREIGN KEY (`PriceID`) REFERENCES `Price` (`PriceID`);

ALTER TABLE `Reservation` ADD FOREIGN KEY (`DiscountID`) REFERENCES `Discount` (`DiscountID`);
