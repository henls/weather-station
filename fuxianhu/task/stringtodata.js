var Device=require('onedevice');
var ssd1306 = new Device({
    description: 'ssd1306',
    width: 128,
    height: 64,
    address: 0x3c,
    device: '/dev/i2c-1'
});
ssd1306.drawPNG('path/to/image.png', false, function(error){
    if (error) {
        console.log(error);
    }else{
        console.log('显示PNG图片完成');
    }
});