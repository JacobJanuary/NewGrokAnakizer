-- Создание базы данных
        CREATE         DATABASE IF NOT EXISTS crypto_analyzer 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE         crypto_analyzer;

-- Таблица твитов
        CREATE TABLE IF NOT EXISTS tweets         (             id             INT             AUTO_INCREMENT             PRIMARY             KEY,             url             VARCHAR         (             500         ) NOT NULL UNIQUE,
            tweet_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            isGrok BOOLEAN DEFAULT NULL,             INDEX idx_created_at         (             created_at         ),
            INDEX idx_is_grok         (             isGrok         ),
            INDEX idx_created_grok         (             created_at,             isGrok         )
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица анализа
        CREATE TABLE IF NOT EXISTS tweet_analysis         (             id             INT             AUTO_INCREMENT             PRIMARY             KEY,             url             VARCHAR         (             500         ) NOT NULL,
            type VARCHAR         (             50         ) NOT NULL,
            title VARCHAR         (             200         ) DEFAULT '',
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,             INDEX idx_created_at         (             created_at         ),
            INDEX idx_type         (             type         ),
            INDEX idx_url         (             url         ),
            INDEX idx_created_type         (             created_at,             type         )
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;                