- Author: Ji Yang
- Contact: yangji9181[AT]gmail.com
- Changelog: 
    - 2014.07.25 Initial version.
    - 2014.08.07 Edited by Ji Yang
 
####一,URL说明
url相对路径  | HTTP variable | 功能 
----------     | ----------| -------- 
/fetchcurriculum/     	|    POST   |   抓取课表
/getcourselist/		    |    POST   |   获取课程列表

####二，数据格式

(1)抓取课表：/fetchcurriculum/	-X GET

请求数据格式：
	
	{
	    token:		string,		//required
	    eas_id:		string,		//教务系统账号，required
	    eas_pwd:	string,		//教务系统密码，required
	    semester:	string		//学期代号，可通过univinfo模块的getsemesters接口获得，required
	}
	

返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
	}
	
(2)获取课程列表：/getcourselist/		-X GET

请求数据格式：

	{
		token: 	string,			//required
	}

返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:	{
				user:		integer,
				section:	integer,
				grade:		string,
				status:		integer
				}
	}
	

####三，返回数据说明
#####1，status 字段
status code| 功能
---------- | ------------- 
"success" |    请求成功 
"fail"    |    请求失败（客户端提交数据错误等）    
"error"   |    服务器错误（数据库不一致等异常情况）

#####2，message 字段
用于请求发生错误时返回错误信息

#####3，data
部分请求中用于返回客户端所需的数据。

####四，解释说明
- 由于抓取学校信息和分析工作量太大，目前只支持UCB，其余学校会引发university not supported错误。
- 目前获取课程列表主要返回section id，这个id可用于univinfo模块getcourse, getsection, getlectures接口获取详细的课程信息。