SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = 'Asia/Beirut';

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'company', 'admin') DEFAULT 'student',
    age INT,
    date_of_birth DATE,
    bio TEXT,
    profile_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    description TEXT
) ENGINE=InnoDB;

CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB;

CREATE TABLE quizzes (
    quiz_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_text TEXT NOT NULL,
    difficulty INT DEFAULT 1,
    time_limit INT DEFAULT 30,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE choices (
    choice_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    choice_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE user_quiz_attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_id INT NOT NULL,
    score INT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE answers (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    attempt_id INT NOT NULL,
    question_id INT NOT NULL,
    choice_id INT NOT NULL,
    FOREIGN KEY (attempt_id) REFERENCES user_quiz_attempts(attempt_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (choice_id) REFERENCES choices(choice_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE user_skill_scores (
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    score_percentage INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, skill_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE certificates (
    certificate_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    issuer VARCHAR(150),
    issue_date DATE,
    certificate_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    rater_user_id INT NOT NULL,
    rated_user_id INT NOT NULL,
    score INT CHECK (score BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rater_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (rated_user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE badges (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE=InnoDB;

CREATE TABLE user_badges (
    user_id INT NOT NULL,
    badge_id INT NOT NULL,
    awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, badge_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(badge_id) ON DELETE CASCADE
) ENGINE=InnoDB;

COMMIT;
