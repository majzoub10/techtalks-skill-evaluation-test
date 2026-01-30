SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = 'Asia/Beirut';

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student','company','admin') DEFAULT 'student',
    bio TEXT,
    profile_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE certificates (
    certificate_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    issuer VARCHAR(150),
    issue_date DATE,
    certificate_url VARCHAR(255),
    CONSTRAINT fk_certificates_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE quizzes (
    quiz_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_id INT NOT NULL,
    title VARCHAR(100),
    time_limit INT DEFAULT 300,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_quizzes_skill
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_text TEXT NOT NULL,
    difficulty_level INT NOT NULL,
    points INT DEFAULT 10,
    CONSTRAINT fk_questions_quiz
        FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE choices (
    choice_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    choice_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_choices_question
        FOREIGN KEY (question_id) REFERENCES questions(question_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_quiz_attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_id INT NOT NULL,
    total_score INT,
    time_taken INT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_attempts_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_attempts_quiz
        FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE answers (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    attempt_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_choice_id INT NOT NULL,
    CONSTRAINT fk_answers_attempt
        FOREIGN KEY (attempt_id) REFERENCES user_quiz_attempts(attempt_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_answers_question
        FOREIGN KEY (question_id) REFERENCES questions(question_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_answers_choice
        FOREIGN KEY (selected_choice_id) REFERENCES choices(choice_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_skill_scores (
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    confidence_score DECIMAL(5,2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, skill_id),
    CONSTRAINT fk_user_skill_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_user_skill_skill
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;
