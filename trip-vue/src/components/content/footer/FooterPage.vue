<template>
  <div id="footer_page">
    <div class="links">
      <div class="abouts">
        <div><a>关于我们</a></div>
        <div><a>联系我们</a></div>
        <div><a>隐私政策商标声明</a></div>
        <div><a>服务协议</a></div>
        <div><a>网络信息侵权通知指引</a></div>
        <div><a>旅游网服务监督员</a></div>
      </div>

    </div>
    <div class="wx">
      <img src="~assets/img/footer/wx1.jpg" alt="">
    </div>
    <div class="copyright">
      Copyright © 2024byBupt2021211316_1201 All rights reserved.
    </div>
  </div>
</template>
<script>
export default {
  
}
</script>
<style>
  #footer_page {
    width: 100%;
    height: 400px;
    background-color: rgb(35, 22, 22);
    position: relative;
  }
  .links {
    position: relative;
    width: 500px;
    height: 370px;
    left: 330px;
    display: flex;
  }
  .abouts, .server {
    margin-top: 25px;
  }
  .abouts > div, .server > div{
    margin-top: 22px;
    font-size: 14px;
    color: rgb(105, 91, 91);
  }
  .server {
    margin-left: 50px;
  }
  .abouts > div:hover, .server > div > a:hover {
    cursor: pointer;
    text-decoration: underline;
  }
  .server > div :nth-child(2) {
    margin-left: 10px;
  }
  .wx {
    width: 200px;
    height: 200px;
    position: absolute;
    top: 50px;
    right: 25%;
  }
  .wx img {
    width: 100%;
    height: 100%;
  }
  .copyright {
    width: 100%;
    text-align: center;
    color: rgb(142, 117, 117);
    font-size: 14px;
  }
</style>