-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2024 at 11:53 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tintots_kindergarden`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance_record`
--

CREATE TABLE `attendance_record` (
  `id` int(100) NOT NULL,
  `subject` varchar(10) NOT NULL,
  `stud_id` int(11) NOT NULL,
  `student` varchar(20) NOT NULL,
  `time_recorded` datetime NOT NULL DEFAULT current_timestamp(),
  `attendance` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_record`
--

INSERT INTO `attendance_record` (`id`, `subject`, `stud_id`, `student`, `time_recorded`, `attendance`) VALUES
(59, 'Living Ski', 20240205, 'try2', '2024-03-12 10:46:08', 1),
(60, 'Mathematic', 20240204, 'try1', '2024-03-13 11:09:00', 0),
(61, 'Science', 20240204, 'try1', '2024-03-13 11:21:20', 0),
(62, 'Mathematic', 20240204, 'try1', '2024-03-13 11:26:56', 0),
(63, 'Science', 20240204, 'try1', '2024-03-13 11:31:51', 1),
(64, 'Living Ski', 20240205, 'try2', '2024-03-13 14:17:11', 1),
(65, 'Science', 20240204, 'try1', '2024-03-13 14:17:37', 1),
(66, 'Living Ski', 20240205, 'try2', '2024-03-13 17:18:04', 1),
(67, 'Mathematic', 20240204, 'try1', '2024-03-16 22:30:02', 0),
(68, 'Mathematic', 20240204, 'try1', '2024-03-17 12:43:57', 1),
(69, 'Science', 35, 'Michael Tan', '2024-03-17 13:08:23', 0),
(70, 'Science', 38, 'Liam Tan', '2024-03-17 13:08:23', 0),
(71, 'Science', 41, 'Olivia Goh', '2024-03-17 13:08:23', 0),
(72, 'Science', 44, 'Jane Smith', '2024-03-17 13:08:23', 1),
(73, 'Science', 47, 'Michael Tan', '2024-03-17 13:08:23', 1),
(74, 'Science', 50, 'Liam Tan', '2024-03-17 13:08:23', 1),
(75, 'Science', 53, 'Olivia Goh', '2024-03-17 13:08:23', 0),
(76, 'Science', 56, 'Jane Smith', '2024-03-17 13:08:23', 0),
(77, 'Mathematic', 35, 'Michael Tan', '2024-03-17 14:08:46', 1),
(78, 'Mathematic', 38, 'Liam Tan', '2024-03-17 14:08:46', 1),
(79, 'Mathematic', 41, 'Olivia Goh', '2024-03-17 14:08:46', 0),
(80, 'Mathematic', 44, 'Jane Smith', '2024-03-17 14:08:46', 0),
(81, 'Mathematic', 47, 'Michael Tan', '2024-03-17 14:08:46', 0),
(82, 'Mathematic', 50, 'Liam Tan', '2024-03-17 14:08:46', 0),
(83, 'Mathematic', 53, 'Olivia Goh', '2024-03-17 14:08:46', 0),
(84, 'Mathematic', 56, 'Jane Smith', '2024-03-17 14:08:46', 0),
(85, 'Science', 35, 'Michael Tan', '2024-03-17 18:27:54', 1),
(86, 'Science', 38, 'Liam Tan', '2024-03-17 18:27:54', 1),
(87, 'Science', 41, 'Olivia Goh', '2024-03-17 18:27:54', 1),
(88, 'Science', 44, 'Jane Smith', '2024-03-17 18:27:54', 1),
(89, 'Science', 47, 'Michael Tan', '2024-03-17 18:27:54', 1),
(90, 'Science', 50, 'Liam Tan', '2024-03-17 18:27:54', 1),
(91, 'Science', 53, 'Olivia Goh', '2024-03-17 18:27:54', 1),
(92, 'Science', 56, 'Jane Smith', '2024-03-17 18:27:54', 1);

-- --------------------------------------------------------

--
-- Table structure for table `marks_record`
--

CREATE TABLE `marks_record` (
  `id` int(10) NOT NULL,
  `subject` varchar(225) NOT NULL,
  `stud_id` varchar(225) NOT NULL,
  `stud_name` varchar(225) NOT NULL,
  `midterm` float NOT NULL,
  `final` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `marks_record`
--

INSERT INTO `marks_record` (`id`, `subject`, `stud_id`, `stud_name`, `midterm`, `final`) VALUES
(6, 'Art', '20240204', 'try1', 0, 0),
(7, 'Mathematics', '20240204', 'try1', 80, 70),
(8, 'Science', '20240204', 'try1', 50, 70),
(9, 'Living Skills', '20240205', 'try2', 0, 0),
(10, 'Music', '20240205', 'try2', 0, 0),
(11, 'Bahasa Melayu', '20240208', 'cheche', 0, 0),
(12, 'English', '20240208', 'cheche', 29, 0);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(5) NOT NULL,
  `name` varchar(225) NOT NULL,
  `contact` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `age` varchar(4) NOT NULL,
  `address` text NOT NULL,
  `email` varchar(225) NOT NULL,
  `qualification` text NOT NULL,
  `position` varchar(225) NOT NULL,
  `department` varchar(225) NOT NULL,
  `salary` int(10) NOT NULL,
  `profile_pic` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`id`, `name`, `contact`, `password`, `age`, `address`, `email`, `qualification`, `position`, `department`, `salary`, `profile_pic`) VALUES
(1, 'Shaihy', '0102002', 'haha_no_pswd', '23', 'No.30, Jalan Sana, \r\nTaman Situ 34500.', 'haha@gg.com', 'Skilled in playing piano, flute, and guitar\r\nAn enthusiastic and engaging storyteller\r\nExcellent at interacting with children as young as 4 years old\r\nExtreme patience and understanding\r\nGreat organisational skills\r\nKnowledgeable in MS Office applications', 'Teacher', 'Academic', 2333, '\\xampp\\htdocs\\tintots\\placeholder.jpg'),
(2, 'hooi yee', '0102002', 'ggg', '23', '0102002', 'gg.com', '-', 'teacher', 'teaching', 2333, '\\xampp\\htdocs\\tintots\\Background.png'),
(20002020, 'admin', '234567890', 'gg', '34', 'sdfgh', 'hahahaha@7788.com', '-', 'admininstrator', 'admin', 2435, ''),
(2004010101, 'halo', '01000100101', 'halo', '23', 'taman halo', 'halo@gg.com', 'halo bye', 'teacher', 'academic', 0, '\\xampp\\htdocs\\tintots\\Background.png');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `name` varchar(225) DEFAULT NULL,
  `age` int(10) DEFAULT NULL,
  `contact` varchar(25) DEFAULT NULL,
  `address` varchar(225) DEFAULT NULL,
  `enroll_date` date DEFAULT NULL,
  `year` int(2) DEFAULT NULL,
  `emergency_contact` varchar(25) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL,
  `annual_review` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`id`, `name`, `age`, `contact`, `address`, `enroll_date`, `year`, `emergency_contact`, `profile_pic`, `annual_review`) VALUES
(34, 'Sarah Lee', 5, '0192837465', 'No. 567, Persiaran MNO, 30010, Penang', '2022-04-05', 1, '0161616161', NULL, ''),
(35, 'Michael Tan', 3, '0165478923', 'No. 890, Jalan PQR, 60020, Malacca', '2022-05-10', 2, '0131313131', NULL, ''),
(36, 'Lisa Wong', 4, '0134689752', 'No. 234, Jalan GHI, 70030, Sabah', '2022-06-15', 3, '0171717171', NULL, ''),
(37, 'Emma Lee', 4, '0123456789', 'No. 1, Jalan ABC, 43000, Selangor', '2022-01-01', 1, '0123456789', NULL, ''),
(38, 'Liam Tan', 5, '0987654321', 'No. 2, Lebuh XYZ, 50450, Kuala Lumpur', '2022-02-15', 2, '0198765432', NULL, ''),
(39, 'Mia Wong', 4, '0112233445', 'No. 3, Lorong DEF, 80000, Johor Bahru', '2022-03-20', 3, '0189898989', NULL, ''),
(40, 'Noah Lim', 5, '0192837465', 'No. 4, Persiaran MNO, 30010, Penang', '2022-04-05', 1, '0161616161', NULL, ''),
(41, 'Olivia Goh', 4, '0165478923', 'No. 5, Jalan PQR, 60020, Malacca', '2022-05-10', 2, '0131313131', NULL, ''),
(42, 'Ethan Ng', 5, '0134689752', 'No. 6, Jalan GHI, 70030, Sabah', '2022-06-15', 3, '0171717171', NULL, ''),
(43, 'John Doe', 5, '0123456789', 'No. 123, Jalan ABC, 43000, Selangor', '2022-06-15', 1, '0123456789', NULL, ''),
(44, 'Jane Smith', 3, '01987654321', 'No. 456, Lebuh XYZ, 50450, Kuala Lumpur', '2022-02-15', 2, '0198765432', NULL, ''),
(45, 'Ahmad Bin', 5, '0112233445', 'No. 789, Lorong DEF, 80000, Johor Bahru', '2022-03-20', 3, '0189898989', NULL, ''),
(46, 'Sarah Lee', 5, '0192837465', 'No. 567, Persiaran MNO, 30010, Penang', '2022-04-05', 1, '0161616161', NULL, ''),
(47, 'Michael Tan', 3, '0165478923', 'No. 890, Jalan PQR, 60020, Malacca', '2022-05-10', 2, '0131313131', NULL, ''),
(48, 'Lisa Wong', 4, '0134689752', 'No. 234, Jalan GHI, 70030, Sabah', '2022-06-15', 3, '0171717171', NULL, ''),
(49, 'Emma Lee', 4, '0123456789', 'No. 1, Jalan ABC, 43000, Selangor', '2022-01-01', 1, '0123456789', NULL, ''),
(50, 'Liam Tan', 5, '0987654321', 'No. 2, Lebuh XYZ, 50450, Kuala Lumpur', '2022-02-15', 2, '0198765432', NULL, ''),
(51, 'Mia Wong', 4, '0112233445', 'No. 3, Lorong DEF, 80000, Johor Bahru', '2022-03-20', 3, '0189898989', NULL, ''),
(52, 'Noah Lim', 5, '0192837465', 'No. 4, Persiaran MNO, 30010, Penang', '2022-04-05', 1, '0161616161', NULL, ''),
(53, 'Olivia Goh', 4, '0165478923', 'No. 5, Jalan PQR, 60020, Malacca', '2022-05-10', 2, '0131313131', NULL, ''),
(54, 'Ethan Ng', 5, '0134689752', 'No. 6, Jalan GHI, 70030, Sabah', '2022-06-15', 3, '0171717171', NULL, ''),
(55, 'John Doe', 5, '0123456789', 'No. 123, Jalan ABC, 43000, Selangor', '2022-06-15', 1, '0123456789', NULL, ''),
(56, 'Jane Smith', 3, '01987654321', 'No. 456, Lebuh XYZ, 50450, Kuala Lumpur', '2022-02-15', 2, '0198765432', NULL, ''),
(57, 'Ahmad Bin', 5, '0112233445', 'No. 789, Lorong DEF, 80000, Johor Bahru', '2022-03-20', 3, '0189898989', NULL, '');

-- --------------------------------------------------------

--
-- Table structure for table `stud_ms`
--

CREATE TABLE `stud_ms` (
  `id` int(8) NOT NULL,
  `name` varchar(225) NOT NULL,
  `age` int(5) NOT NULL,
  `contact` varchar(225) NOT NULL,
  `address` varchar(225) NOT NULL,
  `enrol_date` date NOT NULL,
  `year` int(4) NOT NULL,
  `subject` varchar(225) NOT NULL,
  `annual_review` varchar(225) NOT NULL,
  `profile_pic` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stud_ms`
--

INSERT INTO `stud_ms` (`id`, `name`, `age`, `contact`, `address`, `enrol_date`, `year`, `subject`, `annual_review`, `profile_pic`) VALUES
(20240204, 'try1', 8, '123456', 'hhh', '2024-03-06', 2, 'mathematics, science, english', 'gooooooooooood', '\\xampp\\htdocs\\tintots\\placeholder.jpg'),
(20240205, 'try2', 8, '123456', 'hhh', '2024-03-06', 3, 'trigonometry', '', '\\xampp\\htdocs\\tintots\\placeholder.jpg'),
(20240208, 'cheche', 3, '45678', 'sadfghj', '2024-03-12', 1, '', '', '\\xampp\\htdocs\\tintots\\placeholder.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject` (
  `code` varchar(10) NOT NULL,
  `name` varchar(45) NOT NULL,
  `year` int(3) NOT NULL,
  `assigned` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subject`
--

INSERT INTO `subject` (`code`, `name`, `year`, `assigned`) VALUES
('AT02', 'Art', 2, 2004010101),
('BM01', 'Bahasa Melayu', 1, 2),
('EG01', 'English', 1, 2),
('LS03', 'Living Skills', 3, 1),
('MS03', 'Music', 3, 1),
('MT02', 'Mathematics', 2, 2004010101),
('PE03', 'Physical Education', 3, 2),
('SC02', 'Science', 2, 2004010101);

-- --------------------------------------------------------

--
-- Table structure for table `time_slot`
--

CREATE TABLE `time_slot` (
  `id` int(30) NOT NULL,
  `subject` varchar(10) NOT NULL,
  `day` varchar(20) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_slot`
--

INSERT INTO `time_slot` (`id`, `subject`, `day`, `start_time`, `end_time`) VALUES
(1, 'AT02', 'Monday', '13:30:24.993000', '15:00:00.000000'),
(2, 'AT02', 'Tuesday', '08:00:00.000000', '09:00:00.000000'),
(3, 'BM01', 'Monday', '08:00:00.000000', '09:00:00.000000'),
(4, 'BM01', 'Wednesday', '08:00:00.000000', '09:30:00.000000'),
(5, 'LS03', 'Wednesday', '15:00:00.000000', '16:00:00.000000'),
(6, 'EG01', 'Wednesday', '14:00:00.000000', '15:00:00.000000'),
(7, 'LS03', 'Tuesday', '10:00:00.000000', '11:00:00.000000'),
(8, 'MT02', 'Thursday', '08:00:00.000000', '09:00:00.000000'),
(9, 'MT02', 'Thursday', '09:00:00.000000', '08:00:00.000000'),
(10, 'PE03', 'Thursday', '10:00:00.000000', '11:00:00.000000'),
(11, 'PE03', 'Friday', '15:00:00.000000', '16:00:00.000000'),
(12, 'SC02', 'Friday', '10:00:00.000000', '11:00:00.000000'),
(13, 'SC02', 'Thursday', '13:00:00.000000', '14:00:00.000000');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance_record`
--
ALTER TABLE `attendance_record`
  ADD PRIMARY KEY (`id`),
  ADD KEY `subject` (`subject`,`student`),
  ADD KEY `stud_fk` (`student`);

--
-- Indexes for table `marks_record`
--
ALTER TABLE `marks_record`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stud_ms`
--
ALTER TABLE `stud_ms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
  ADD PRIMARY KEY (`code`),
  ADD KEY `Assigned` (`assigned`);

--
-- Indexes for table `time_slot`
--
ALTER TABLE `time_slot`
  ADD PRIMARY KEY (`id`),
  ADD KEY `subject` (`subject`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance_record`
--
ALTER TABLE `attendance_record`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `marks_record`
--
ALTER TABLE `marks_record`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2004010102;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `stud_ms`
--
ALTER TABLE `stud_ms`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20240209;

--
-- AUTO_INCREMENT for table `time_slot`
--
ALTER TABLE `time_slot`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `subject`
--
ALTER TABLE `subject`
  ADD CONSTRAINT `teacher` FOREIGN KEY (`assigned`) REFERENCES `staff` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `time_slot`
--
ALTER TABLE `time_slot`
  ADD CONSTRAINT `subject_foreignkey` FOREIGN KEY (`subject`) REFERENCES `subject` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
