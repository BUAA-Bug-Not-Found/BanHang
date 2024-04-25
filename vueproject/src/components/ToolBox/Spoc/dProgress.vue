<template>
    <div class="progress " :class="'progress--'+ptype">
        <!-- 条形进度条 -->
        <div class="progress-bar__outer" :style="{height:strokeHeight+'px'}">
            <div class="progress-bar__inner" :style="barStyle">
                <!-- 进度条内显示百分比 -->
                <!--<div v-if="textInside" class="progress__text" style="color:white;"> {{percentage}}% </div>-->
            </div>
        </div>
    </div>
</template>
<script>
/* eslint-disable */
export default {
    props:{
        strokeHeight:{
            // 进度条高度
            // required:true,
            type:Number,
            default:10
        },
        percentage:{
            // 进度条百分比
            type:Number,
            default:0,
            required:true,
            valiator(value){
                return value>=0 && value<=100
            },
        },
        status:{
            // 进度条状态：正常状态，成功状态，异常状态
            type:String,
 
        },
        ptype:{
            // 进度条样式：条形，还是圆形
            type:String,
            default:'line',
            validator:val=>['circle','line'].includes(val)
        },
        textInside:{
            // 文字是否內显
            type:Boolean,
            default:false,
        },
        pcolor:{
            // 进度条颜色
            type:String
        },
        cwidth:{
            type:Number,
            default:126,
        }
    },
    computed:{
        progressTextSize(){
            return 9+this.strokeHeight*0.4;
        },
        stroke(){
            let color;
            if(this.pcolor){
                return this.pcolor;
            }
            switch(this.status){
                case 'success':
                    color='#13ce66';
                    break;
                case 'failure':
                    color='#ff4949';
                    break;
                default:
                    color='#20a0ff';
                    break;
            }
            return color;
        },
        barStyle(){
            // 计算属性调用其他计算属性，必须加this关键字，否则找不到
            return {width:this.percentage+'%',backgroundColor:this.stroke}
        },
        iconCls(){
            if( this.ptype ==='line'){
                // 如果是线性进度条
                return this.status ==='success'?'icon-circle-check':'icon-circle-close';
            }else{
                return this.status ==='success'?'icon-check':'icon-close';
            }
        },
        trackPath(){
            const radius = 50-this.relativeStrokeHeight/2;
            return 'M 50 50 m 0 -'+radius+' a '+radius+' '+radius+' 0 1 1 0 '+radius*2+' a '+radius+' '+radius+' 0 1 1 0 -'+radius*2+' ' ;
        },
        relativeStrokeHeight(){
            return this.strokeHeight*100 / this.cwidth;
        },
        perimeter(){
            const radius = 50-this.relativeStrokeHeight/2;
            return 2*Math.PI*radius;
        },
        circlePathStyle(){
            const perimeter = this.perimeter;
            return{
                strokeDasharray:''+perimeter+'px,'+perimeter+'px',
                strokeDashoffset:(1-this.percentage/100)*perimeter+'px',
 
            }
        }
    }
}
</script>
<style>
    .progress{
        margin: 10px;
        /* border: 1px solid #ffbbff; */
    }
    .progress-bar{
        display:inline-block;
        width: 98%;
        box-sizing: border-box; /* 盒模型的方式 */
        margin-right: -50px;
        padding-right: 50px;
    }
    .progress-bar__outer{
        width: 100%;
        border-radius: 2px;
        background-color: #ebeef5;
    }
    .progress-bar__inner{
        /* width: 60%; */
        background-color: rebeccapurple;
        border-radius: 2px;
        height: 100%;
        transition: width 0.6s ease;
        text-align: right;
        line-height: 80%;
    }
    .progress__text{
        font-size: 12px;
        margin-left: 6px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 5px;
    }
    .icon-circle-close,.icon-close{
        font-family: 'Wingdings' !important;
        color:red;
    }
    .icon-circle-check,.icon-check{
        font-family: 'Wingdings' !important;
        color:seagreen;
    }
 
    .icon-circle-close::before{
        content: '\FD';
    }
    .icon-close::before{
        content: '\FB';
    }
    .icon-circle-check::before{
        content: '\FE';
    }
    .icon-check::before{
        content: '\FC';
    }
    .progress--circle{
        display: inline-block;
        position: relative;
    }
 
    .progress--circle .progress__text{
        position:absolute;
        top:50%;
        transform: translateY(-50%);
        margin-left: 0px;
        text-align: center;
        width: 100%;
    }
 
</style>