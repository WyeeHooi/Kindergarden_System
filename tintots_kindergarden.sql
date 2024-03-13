-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2024 at 10:22 AM
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
(66, 'Living Ski', 20240205, 'try2', '2024-03-13 17:18:04', 1);

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
(7, 'Mathematics', '20240204', 'try1', 80, 90),
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
  `address` varchar(225) NOT NULL,
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
(1, 'Shaif', '0102002', 'haha', '23', 'Taman Haha', 'haha@gg.com', 'Experienced educator with [X] years in [mention settings such as public or private schools], adept at creating engaging lesson plans, fostering inclusive learning environments, and promoting student success. Skilled in [menti', 'Teacher', 'Academic', 2333, '\\xampp\\htdocs\\tintots\\placeholder.jpg'),
(2, 'hooi yee', '0102002', 'ggg', '23', '0102002', 'gg.com', '-', 'teacher', 'teaching', 2333, '\\xampp\\htdocs\\tintots\\Background.png');

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
('AT02', 'Art', 2, 2),
('BM01', 'Bahasa Melayu', 1, 2),
('EG01', 'English', 1, 2),
('LS03', 'Living Skills', 3, 1),
('MS03', 'Music', 3, 1),
('MT02', 'Mathematics', 2, 1),
('PE03', 'Physical Education', 3, 2),
('SC02', 'Science', 2, 1);

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
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `marks_record`
--
ALTER TABLE `marks_record`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
