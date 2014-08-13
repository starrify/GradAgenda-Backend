- Author: Ji Yang
- Contact: yangji9181[AT]gmail.com
- Changelog: 
    - 2014.07.10 Initial version.
    - 2014.08.01 Edited by Ji Yang
 
####一,URL说明
url相对路径  | HTTP variable | 功能 
----------     | ----------| -------- 
/getuniversities/ 	|    POST	|   搜索学校
/getmajors/		   	|    POST	|   搜索专业
/getprofessors/		|    POST	|   搜索教授
/getsemesters/		|    POST	|   搜索学期
/getcourse/			|    POST	|   搜索课程信息
/getsection/		|    POST	|   搜索section信息
/getlectures/		|    POST	|   搜索lecture信息
/issupported/		|	 POST	|	判断学校是否支持自动同步课程

####二，数据格式

(1)搜索学校：/getuniversities/	

请求数据格式：
	
	{
	    query:  string,		//optional
	    page:	integer,	//optional, default 1
	    items:	integer		//optional, default 15
	}

返回数据格式：

	JSON:
	{	status:		string,
		message:	string,
		data: {
			page:	integer,
			total:	integer,
			data:  {
				id: 	integer,
				fullname:	string,
				shortname:	string
				}
			}
	}
	
	
(2)搜索专业：/getmajors/	

请求数据格式：

	{
		query:  string,		//optional
		page:	integer,	//optional, default 1
	    items:	integer		//optional, default 15
	}

返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data: {
			page:	integer,
			total:	integer,
			data:  {
				id: 	integer,
				fullname:	string,
				shortname:	string
				}
			}
	}

(3)搜索教授：/getprofessors/	

请求数据格式：

	{
		query:		string,		//optional	
	}
	
返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
						id:			integer,	
						first_name:		string,
						last_name:		string,
						title:			string,
						gender:			string,
						image:			string,
						university:		integer,
						email:			string,
						phone:			string,
						office:			string,
						description:	string,
						rate:			float,
						ratecount:		integer
						
	}
		
(4)搜索学期：/getsemesters/	

请求数据格式：

	{
		university:		string,		//required, shortname		
	}

返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
						id:			integer,	
						name:		string,
						universirty:integer,
						start:	datetime,
						end:	datetime
	}

(5)搜索course信息：/getcourse/ 

请求数据格式：

	{
		sectionid:		string,		//required
	}
	
返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
						id:			integer,	
						fullname:	string,
						shortname:	string,
						university:	integer,
						department:	string
	}

	
(6)搜索section信息：/getsection/

请求数据格式：

	{
		sectionid:		string,		//required
	}
	
返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
						id:			integer,	
						name:		string,
						semester:	integer,
						course:		integer,
						professor:	integer,
						start:		date,
						end:		date,
						description:string,
						rate:		float,
						ratecount:	integer
	}
	
(7)搜索lecture信息：/getlectures/ 

请求数据格式：

	{
		sectionid:		string,		//required
	}
	
返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		{
						id:			integer,	
						section:	integer,
						weekday:	integer,
						starttime:	time,
						endtime:	time,
						start:		date,
						location:	string
	}
	
（8）判断学校是否支持自动同步课程： /issupported/
请求数据格式：

	{
		shortname:		string,		//required
	}
	
返回数据格式：

	JSON:
	{
		status:		string,
		message:	string,
		data:		'true' or 'false (string)
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
- 课程信息分为course\section\lecture这样的三级结构，第一级course仅包括fullname和shortname，分别为课程去全称与代号，课程社区基于这一级；第二级section为具体课程，包括始末时间、任课教授等信息；第三级lecture实际为虚拟层，用于处理一门课有多个上课时间等情况，包括上课的星期号（1-7）与上课地点等信息。目前具体信息的获取方式为通过getcourselist接口得到sectionid后逐一调用getcourse\getsection\getlectures模块获取。
- 本模块所有接口不需要传入token
#####1，/getuniversities/ 
传入query可选，如传入则快速搜索fullname及shortname匹配项，不传入则返回所有学校列表
#####2，/getmajors/
同getuniversities
#####3，/getprofessors/
同getuniversities
#####4，/getsemesters/
传入学校shortname，得到semester列表，让用户选择要导入的semester后传入fetchcurriculum接口获取相应学期的课表
 
	
	