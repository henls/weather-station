const express=require('express');
const fs=require('fs');
const path=require('path');
var server=express();
server.use(express.static(path.join(__dirname, 'www')));
//console.log(__dirname.constructor);
server.set('views',__dirname+'/views');
server.set('view engine','ejs');
server.use(require('./router/web.js'));

/*server.use(function (req,res) {
    var file_name = '../task'+req.url;
    console.log(file_name);

    fs.readFile(file_name, 'binary', function (err, data) {
        //res.writeHead(200,{'Context-Type':'image/jpeg'})
        //console.log(data);
        if (err) {
            res.write('404');
        } else {
            //var buffer=new Buffer(data)
            //res.write(data, "binary")
            res.write(data,'binary');
        }

        res.end();
    })
});*/
server.listen(8080,function () {
    console.log('服务器已启动');
});