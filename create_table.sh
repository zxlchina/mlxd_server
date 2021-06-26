
mysql mlxd -uroot -pzxlchina -e "
create table order_list 
(
 id BIGINT AUTO_INCREMENT ,
 out_trade_no varchar(1024) NOT NULL COMMENT '订单号' ,
 buyer_openid varchar(1024) NOT NULL COMMENT '用户id' ,
 remark varchar(1024) COMMENT '用户备注' ,
 buyer_nick varchar(1024 )COMMENT '用户昵称' ,
 promotion_fee BIGINT ,
 payer_is_leaguer boolean ,
 total_fee bigint COMMENT '总金额' ,
 shop_buyer_count BIGINT ,
 total_refund_fee BIGINT ,
 used_points boolean ,
 weeklyup boolean ,
 time_end BIGINT ,
 has_promotion boolean ,
 time_start BIGINT ,
 order_fee BIGINT ,
 shop_id BIGINT ,
 buyer_headimgurl varchar(1024) ,
 settlement_total_fee BIGINT ,
 mlj boolean ,
 order_source varchar(1024) ,
 points_deduct_fee BIGINT ,
 trade_state varchar(1024) ,
 create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
 update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

 PRIMARY KEY(id),
 unique key uniq (out_trade_no)

)ENGINE=InnoDB DEFAULT CHARSET=utf8 "
