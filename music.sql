CREATE TABLE `netease_music_artists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `artist_id` int(11) NOT NULL UNIQUE,
  `brief_desc` varchar(1024) NOT NULL,
  `pic_url` varchar(128) DEFAULT NULL,
  `pic_id` varchar(32) NOT NULL,
  `mv_size` int(11) DEFAULT NULL,
  `album_size` int(11) DEFAULT NULL,
  `music_size` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
