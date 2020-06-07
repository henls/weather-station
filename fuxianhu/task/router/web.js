const express=require('express');
const Router=express.Router();
const fs=require('fs');
var https = require('https');
var iconv = require('iconv-lite');
var date = new Date();
var dateNow= date.toLocaleDateString();
//dateNow=dateNow.split('-')[0]+'-0'+dateNow.split('-')[1]+'-0'+dateNow.split('-')[2]
dateYear=dateNow.split('-')[0]
var month_=dateNow.split('-')[1]
var day_ = dateNow.split('-')[2]

switch(month_.length)
{
    case 2:switch (day_.length){case 2:dateNow=dateNow.split('-')[0]+'-'+dateNow.split('-')[1]+'-'+dateNow.split('-')[2];break;
                                case 1:dateNow=dateNow.split('-')[0]+'-'+dateNow.split('-')[1]+'-0'+dateNow.split('-')[2];break; };break;
    case 1:switch (day_.length){case 2:dateNow=dateNow.split('-')[0]+'-0'+dateNow.split('-')[1]+'-'+dateNow.split('-')[2];break;
                                case 1:dateNow=dateNow.split('-')[0]+'-0'+dateNow.split('-')[1]+'-0'+dateNow.split('-')[2];break;};break;

}
//if (month_.length<2 and day_.length<2){
//dateNow=dateNow.split('-')[0]+'-0'+dateNow.split('-')[1]+'-0'+dateNow.split('-')[2]
//}
//tiaoshi
//server=express();
var js=[];
Router.get('/metestat/data',function (req,res,next) {
    //
    var result;
    //var url='https://services.swpc.noaa.gov/products/latest-xray-event.json';
    var url='https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json'
    https.get(url,function(res1){
    var datas=[];
    var size=0;
    res1.on('data',function(data1){
    datas.push(data1);
    size+=data1.length;
    });
    res1.on('end',function(){
    var buff = Buffer.concat(datas,size);
    result = iconv.decode(buff,'utf8');
    result = result.slice(1,-1);
    //console.log(result);
    var obj=JSON.parse(result);
    for(var item in obj){
        var jvalue = obj[item];
        js.push(jvalue);
        
    }
    
  
});
}).on('error',function(err1){
    //Logger.error(err1.stack);
    //callback.apply(null);

});
    /*var current=js[10];
    var begin = js[0];
    var max = js[2];
    var end = js[4];
    var begin_class = js[1];
    var max_class = js[3];
    var end_class = js[5];
    var current_class = js[8];
    var ratio = js[9];
    var xrlong = js[6];*/
    var current=js[0];
    var begin = js[4];
    var max = js[6];
    var end = js[9];
    var begin_class = js[5];
    var max_class = js[7];
    var end_class = js[12];
    var current_class = js[2];
    var ratio = js[3];
    var xrlong = js[8];
    //console.log(js);
    //file_name=__dirname+'/data.csv';
    //file_name = '/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv'
    file_name = '/home/pi/Desktop/communication/latest.csv'
    //file_name = '/home/pi/Desktop/communication/'+dateNow+'/data'+dateNow+'.csv'
    //file_name='/data.csv';
    //var new_data,tem,hum,press,spreed,dir_wind,dew,rad,new_number;
    var new_data,tem,hum,press,speed,dir_wind,dew,rad,rain,new_number;
    list =[1];
    //当前时间
    var yearNow;
    var monthNow;
    var r0;
    var obsertime;

    //监测x-ray event
   // fs.readFile('/home/pi/Desktop/fuxianhu/task/router/x_ray_event.txt',function(err,data){
   //     if(err){
   //      console.log('文件读取错误');
   //      }else{
              //console.log(data,begin);
              //console.log(iconv.decode(data,'utf8')=='undefined')
              //console.log(begin)
   //           if(iconv.decode(data,'utf8')!=begin && iconv.decode(data,'utf8')!='undefined' && begin!='undefined'){
              
   //            fs.writeFile('/home/pi/Desktop/fuxianhu/task/router/x_ray_event.txt',begin,function(err){
   //            if(err) throw err;
   //             console.log('发生一次事件');
   //            });
   //           }

   //      }
   ray = fs.readFileSync('/home/pi/Desktop/fuxianhu/task/router/x_ray_event.txt').toString()
   //console.log(ray)
   //console.log(begin)
   if (ray!=begin && begin!= undefined){
   fs.writeFile('/home/pi/Desktop/fuxianhu/task/router/x_ray_event.txt',begin,function(err){
               if(err) throw err;
                console.log('发生一次事件');
               });
}
   r0file = '/home/pi/Desktop/fuxianhu/r0.txt'
   fs.readFile(r0file,function(err,data){
	if(err){
	consloe.log('文件读取失败');
	}
	else{
	r0content = data.toString().split('\t');
        obsertime = r0content[0][1]+':'+r0content[0].substr(2,2)+':'+r0content[0].substr(4,2);
        r0 = r0content[1];
	}
	})


    //定时程序
    fs.readFile(file_name,function (err, data) {
        if (err){
            var flag='未接收到气象数据'
        }else {
            
            /*data = data.toString();
            
            list=data.split('\n');
            console.log(list)
            //console.log(list.length);
            new_number=list.length-2;
            new_data=list[new_number];
            new_data=new_data.split('\t');
            tem=new_data[0];
            hum=new_data[1];
            press=new_data[3];
            spreed=new_data[5];
            dir_wind=new_data[7];
            dew=new_data[8];*/
            /*********** */
            /*data = data.toString();
            //data=data.slice(1,-1)
            list = data.split('\n')
            //console.log(list)
            //console.log(list.length);
            new_number=list.length-2;
            new_data=list[new_number];

            new_data=new_data.slice(1,-1).split(',');*/
            data = data.toString();
            //data=data.slice(1,-1)
            
            list = data.split('\n')
            
            //console.log(list.length);
            new_number=list.length-2;
            
            new_data=list[new_number];
            //console.log(new_data)
            //new_data=new_data.slice(1,-1).split(',');
            new_data=new_data.split(',');
            yearNow=new_data[0].slice(1,-1);
            monthNow=new_data[1].slice(2,-1);
            speed=new_data[2];
            rain=new_data[3];
            tem=new_data[4];
            press=new_data[5];
            rad=new_data[6];
            dir_wind=new_data[7];
            hum=new_data[8];
            dew=new_data[9];
            /*********** */
             
            var date;
            date=Date();
            
            res.render('web',{
                title:'抚仙湖气象站数据',
                head:'系统测试',
                data:{
                    yearNow:yearNow,                   
                    monthNow:monthNow,
                    tem:tem,
                    hum:hum,
                    press:press,
                    speed:speed,
                    dir_wind:dir_wind,
                    dew:dew,
                    rad:rad,
                    rain:rain,
                    date:date,
                    current:current,
                    begin:begin,
                    max:max,
                    end:end,
                    begin_class:begin_class,
                    max_class:max_class,
                    end_class:end_class,
                    current_class:current_class,
                    ratio:ratio,
                    xrlong:xrlong,
                    r0:r0,
                    obsertime:obsertime
                }
            });
        js=[];
        }
    });
    


});
//server.use(router);
//server.listen(8080);
module.exports=Router;
