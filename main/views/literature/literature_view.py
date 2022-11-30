import json
import traceback

from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from main.models.models import Literature


class LiteratureView(APIView):
    # permission_classes = ([IsAuthenticated])

    # 按照传入的参数进行查询
    def get(self, request):
        arg = request.GET
        try:
            lit_id = arg.get("lit_id")
            lit_ch_title = arg.get("lit_ch_title")
            lit_en_title = arg.get("lit_en_title")
            lit_category = arg.get("lit_category")
            fig_id = arg.get("fig_id")
            kwargs = {}
            if lit_id:
                kwargs["lit_id"] = lit_id
            if lit_ch_title:
                kwargs["lit_ch_title__contains"] = lit_ch_title
            if lit_en_title:
                kwargs["lit_en_title__contains"] = lit_en_title
            if lit_category:
                kwargs["lit_category__contains"] = lit_category
            if fig_id:
                kwargs["fig_id"] = fig_id

            qs = Literature.objects.filter(**kwargs) # 按条件筛

            literatureList = [] # 存放查询书籍的结果
            figureList = [] # 存放书籍的作者
            for lit in qs:
                literatureList.append(model_to_dict(lit))
                figureList.append(model_to_dict(lit.fig))

            figureDict = {} # 存放作者id到作者的映射
            for fig in figureList:
                figureDict[fig.get('fig_id')] = fig

            # print(literatureList)

            datas = {
                "literatureList": literatureList,
                "figureDict": figureDict,
            }
            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "查询失败"} ,status=500)

    # 按照传入的参数创建literature对象插入数据库
    def post(self, request):
        arg = request.POST

        # lit_ch_title=测试&lit_en_title=test&lit_category=测试类&lit_published_date=2022-11-07&lit_detail=测试描述&lit_read_times=0&lit_img_address=https://img2.doubanio.com/view/subject/l/public/s34044161.jpg&fig_id=1

        # {
        #     "lit_ch_title": "测试",
        #     "lit_en_title": "test",
        #     "lit_category": "测试类",
        #     "lit_published_date": "2022-11-07",
        #     "lit_detail": "测试描述",
        #     "lit_read_times": "0",
        #     "lit_img_address": "https://img2.doubanio.com/view/subject/l/public/s34044161.jpg",
        #     "fig_id": "0"
        # }

        try:
            lit_ch_title = arg.get("lit_ch_title", "")
            print(lit_ch_title)
            lit_en_title = arg.get("lit_en_title", "")
            print(lit_en_title)
            lit_category = arg.get("lit_category", "")
            print(lit_category)
            # lit_published_date = datetime.strptime(arg.get("lit_published_date", ""), "%Y-%m-%d").date()
            lit_published_date = arg.get("lit_published_date", "")
            print(lit_published_date)
            lit_detail = arg.get("lit_detail", "")
            print(lit_detail)
            lit_read_times = arg.get("lit_read_times")
            print(lit_read_times)
            lit_img_address = arg.get("lit_img_address", "https://img2.doubanio.com/view/subject/l/public/s34044161.jpg")
            print(lit_img_address)
            fig_id = arg.get("fig_id")
            print(fig_id)

            Literature.objects.create(lit_ch_title=lit_ch_title, lit_en_title=lit_en_title, lit_category=lit_category,
                                      lit_published_date=lit_published_date, lit_detail=lit_detail, lit_read_times=lit_read_times,
                                      lit_img_address=lit_img_address, fig_id=fig_id)

            return Response({'msg': "添加成功"}, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "添加失败"}, 500)

    # 按照lit_id查找 然后按照传入的参数修改
    def put(self, request):
        arg = request.data
        try:
            lit_id = arg.get("lit_id")
            lit_ch_title = arg.get("lit_ch_title", "")
            lit_en_title = arg.get("lit_en_title", "")
            lit_category = arg.get("lit_category", "")
            # lit_published_date = datetime.strptime(arg.get("lit_published_date", ""), "%Y-%m-%d").date()
            lit_published_date = arg.get("lit_published_date", "")
            lit_detail = arg.get("lit_detail", "")
            lit_read_times = arg.get("lit_read_times")
            lit_img_address = arg.get("lit_img_address", "https://img2.doubanio.com/view/subject/l/public/s34044161.jpg")
            fig_id = arg.get("fig_id")

            kwargs = {}
            if lit_ch_title:
                kwargs["lit_ch_title"] = lit_ch_title
            if lit_en_title:
                kwargs["lit_en_title"] = lit_en_title
            if lit_category:
                kwargs["lit_category"] = lit_category
            if lit_published_date:
                kwargs["lit_published_date"] = lit_published_date
            if lit_detail:
                kwargs["lit_detail"] = lit_detail
            if lit_read_times:
                kwargs["lit_read_times"] = lit_read_times
            if lit_img_address:
                kwargs["lit_img_address"] = lit_img_address
            if fig_id:
                kwargs["fig_id"] = fig_id

            Literature.objects.filter(lit_id=lit_id).update(**kwargs)

            return Response({'msg': "修改成功"}, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "修改失败"}, 500)

    # 按照lit_id删除 可以批量删除
    def delete(self, request):
        arg = request.GET
        try:
            lit_id_list = arg.get("lit_id_list", "").split(',')
            print(lit_id_list)

            qs = Literature.objects.filter(lit_id__in=lit_id_list)

            datas = []
            for lit in qs:
                datas.append(model_to_dict(lit))

            qs.delete()

            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "删除失败"}, status=500)
