一、该项目实现了判题系统的微服务，该微服务有两个接口，一个是判题机接口，另一第三方网站接口。提供给判题机接口的API，用于判题机获取要判的题目和提交判题结果。
第三方网站接口用于接收提交的要判的代码和异步返回判题结果


二、判题信息字段
第三方系统POST的数据会被保存在数据库中，并等待判题机处理
POST请求的数据格式如下，
{'code':'xxx','lang':'x',test_cases:[{'input':'xxx','output':'xxxx'},{'input':'xxx','output':'xxxx'},'notify':'url to notify']}
各字段的说明：

code为用户的代码，该字段必须存在。
lang为语言类型，该字段必须存在。
test_case为测试用例,该字段必须存在。字段内容以数组的方式进行存储；每一个测试用例包含了input和output选项，input是要输入的数据，output为期望输出的数据
notify为回调函数的网址，该字段不强制存在。如果存在，服务器将会向该网址发送GET请求，标识判题已经完成，第三方客户端即可进行查询

POST返回的数据格式如下
{'problem_id':'234234234','secret':'xdfsfsdfdsf'}
problem_id为系统给这个题目的编号，secret为系统生成的密码，solution和task被用于第三方客户端查询结果

在存储时，会存储更多的状态信息,这些信息会存放在redis中
{
  'problem':{'code':'xxx','lang':'x',test_cases:[{'input':'xxx','output':'xxxx'},{'input':'xxx','output':'xxxx'},'notify':'url to notify']},
  'judge'  :{'problem_id':'234234234','secret':'xdfsfsdfdsf','status':'waiting'},
  'result' :{'status':'OL','message':''}
}





