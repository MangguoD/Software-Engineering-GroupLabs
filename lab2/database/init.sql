-- 创建 users 表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    name TEXT NOT NULL
);

-- 创建 tutor_profile 表
CREATE TABLE tutor_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subjects TEXT NOT NULL,
    city TEXT,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建 student_request 表
CREATE TABLE student_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subject TEXT NOT NULL,
    city TEXT,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建 review 表
CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id INTEGER,
    student_id INTEGER,
    rating INTEGER,
    comment TEXT,
    FOREIGN KEY (tutor_id) REFERENCES tutor_profile(id),
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- 插入示例用户数据（前10条为家教用户，后10条为学生用户）
INSERT INTO users (username, password, role, name) VALUES ('tutor1', '123456', 'tutor', '张伟');
INSERT INTO users (username, password, role, name) VALUES ('tutor2', '123456', 'tutor', '李秀英');
INSERT INTO users (username, password, role, name) VALUES ('tutor3', '123456', 'tutor', '王伟');
INSERT INTO users (username, password, role, name) VALUES ('tutor4', '123456', 'tutor', '张敏');
INSERT INTO users (username, password, role, name) VALUES ('tutor5', '123456', 'tutor', '李娜');
INSERT INTO users (username, password, role, name) VALUES ('tutor6', '123456', 'tutor', '刘洋');
INSERT INTO users (username, password, role, name) VALUES ('tutor7', '123456', 'tutor', '王静');
INSERT INTO users (username, password, role, name) VALUES ('tutor8', '123456', 'tutor', '王芳');
INSERT INTO users (username, password, role, name) VALUES ('tutor9', '123456', 'tutor', '李伟');
INSERT INTO users (username, password, role, name) VALUES ('tutor10', '123456', 'tutor', '陈磊');
INSERT INTO users (username, password, role, name) VALUES ('student1', '123456', 'student', '赵勇');
INSERT INTO users (username, password, role, name) VALUES ('student2', '123456', 'student', '钱涛');
INSERT INTO users (username, password, role, name) VALUES ('student3', '123456', 'student', '孙丽');
INSERT INTO users (username, password, role, name) VALUES ('student4', '123456', 'student', '周敏');
INSERT INTO users (username, password, role, name) VALUES ('student5', '123456', 'student', '吴杰');
INSERT INTO users (username, password, role, name) VALUES ('student6', '123456', 'student', '郑洁');
INSERT INTO users (username, password, role, name) VALUES ('student7', '123456', 'student', '冯梅');
INSERT INTO users (username, password, role, name) VALUES ('student8', '123456', 'student', '陈静');
INSERT INTO users (username, password, role, name) VALUES ('student9', '123456', 'student', '楼华');
INSERT INTO users (username, password, role, name) VALUES ('student10', '123456', 'student', '白凯');

-- 插入示例家教信息（对应用户ID 1-10）
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (1, '数学', '北京', '擅长数学，有5年教学经验。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (2, '英语', '上海', '英语专业毕业，口语流利。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (3, '物理', '广州', '理科硕士，物理教学3年经验。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (4, '化学', '深圳', '重点高中化学老师。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (5, '英语, 数学', '北京', '清华毕业生，可辅导英语和数学。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (6, '生物', '杭州', '生物专业博士研究生。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (7, '语文', '成都', '语文特级教师，20年教龄。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (8, '历史', '南京', '热爱历史，教学风趣幽默。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (9, '地理', '西安', '高中地理老师。');
INSERT INTO tutor_profile (user_id, subjects, city, description) VALUES (10, '数学, 物理', '上海', '重点大学理科专业，可教数学和物理。');

-- 插入示例学生需求（对应用户ID 11-20）
INSERT INTO student_request (user_id, subject, city, description) VALUES (11, '数学', '北京', '需要辅导高一数学。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (12, '英语', '上海', '想提高英语口语能力。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (13, '物理', '广州', '准备物理竞赛辅导。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (14, '化学', '深圳', '需要化学课程补习。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (15, '生物', '杭州', '生物基础较弱，需要一对一辅导。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (16, '英语', '北京', '希望提升英语写作能力。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (17, '历史', '南京', '想了解高考历史要点。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (18, '地理', '西安', '需要地理会考复习辅导。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (19, '语文', '成都', '希望提高作文写作技巧。');
INSERT INTO student_request (user_id, subject, city, description) VALUES (20, '物理', '上海', '寻求物理课业辅导。');

-- 插入示例评价数据
INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (1, 11, 5, '很好的老师');
INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (2, 12, 4, '教学耐心');
INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (3, 13, 5, '知识渊博');
INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (5, 16, 5, '非常专业');
INSERT INTO review (tutor_id, student_id, rating, comment) VALUES (10, 20, 4, '讲解清晰');
