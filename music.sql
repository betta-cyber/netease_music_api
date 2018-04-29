CREATE TABLE `netease_music_artists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `artist_id` int(11) NOT NULL UNIQUE,
  `brief_desc` varchar(1024) DEFAULT NULL,
  `pic_url` varchar(128) DEFAULT NULL,
  `pic_id` varchar(32) NOT NULL,
  `mv_size` int(11) DEFAULT NULL,
  `album_size` int(11) DEFAULT NULL,
  `music_size` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `netease_music_albums` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `artist_id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL UNIQUE,
  `comment_thread_id` varchar(64) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `pic_url` varchar(128) DEFAULT NULL,
  `type` varchar(32) NOT NULL,
  `size` int(11) DEFAULT NULL,
  `publish_time` timestamp DEFAULT 0,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `netease_music_songs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `artist_id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL UNIQUE,
  `comment_thread_id` varchar(64) DEFAULT NULL,
  `description` varchar(1024) NOT NULL,
  `pic_url` varchar(128) DEFAULT NULL,
  `mv_id` int(11) DEFAULT NULL,
  `pop` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `netease_music_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `song_id` int(11) NOT NULL,
  `content` varchar(512) DEFAULT NULL,
  `liked_count` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL UNIQUE,
  `send_time` timestamp DEFAULT 0,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
