import json
import traceback

from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from main.models.models import Figure
from main.models.models import FigureCategory


class FigureView(APIView):
    # permission_classes = ([IsAuthenticated])

    # 按照传入的参数进行查询
    def get(self, request):
        arg = request.GET
        try:
            fig_id = arg.get("fig_id")
            fig_ch_name = arg.get("fig_ch_name")
            fig_en_name = arg.get("fig_en_name")
            fig_gender = arg.get("fig_gender")
            fig_nationality = arg.get("fig_nationality")
            kwargs = {}
            if fig_id:
                kwargs["fig_id"] = fig_id
            if fig_ch_name:
                kwargs["fig_ch_name__contains"] = fig_ch_name
            if fig_en_name:
                kwargs["fig_en_name__contains"] = fig_en_name
            if fig_gender:
                kwargs["fig_gender"] = fig_gender
            if fig_nationality:
                kwargs["fig_nationality"] = fig_nationality

            qs = Figure.objects.filter(**kwargs) # 按条件筛

            figureList = [] # 存放人物查询结果
            fig_idList = [] # 存放人物id
            for fig in qs:
                figureList.append(model_to_dict(fig))
                fig_idList.append(fig.fig_id)

            dict = {} # 为每个查询到的人物id建立映射到人物类别列表
            for fig_id in fig_idList:
                dict[fig_id] = []

            qs = FigureCategory.objects.filter(fig_id__in=fig_idList) # 按照这些人物id查类别表

            for fig_cate in qs: # 建立人物id到人物类别名称列表的映射
                dict[fig_cate.fig_id].append(fig_cate.cate.cate_name)

            for figure in figureList: # 将每个人物的类别名称列表加入到他的figure生成带有人物类别名称列表的完整figureList
                figure['fig_cate'] = dict[figure.get('fig_id')]

            datas = {
                'figureList': figureList,
            }
            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "查询失败"}, 500)

    # 按照传入的参数创建literature对象插入数据库
    def post(self, request):
        arg = request.POST

        try:
            fig_ch_name = arg.get("fig_ch_name")
            print(fig_ch_name)
            fig_en_name = arg.get("fig_en_name")
            print(fig_en_name)
            fig_gender = arg.get("fig_gender", "男")
            print(fig_gender)
            # fig_birthday = datetime.strptime(arg.get("fig_birthday", ""), "%Y-%m-%d").date()
            fig_birthday = arg.get("fig_birthday")
            print(fig_birthday)
            fig_deathday = arg.get("fig_deathday")
            print(fig_deathday)
            fig_day_correction = arg.get("fig_day_correction", 0)
            print(fig_day_correction)
            fig_detail = arg.get("fig_detail")
            print(fig_detail)
            fig_nationality = arg.get("fig_nationality")
            print(fig_nationality)
            fig_province = arg.get("fig_province")
            print(fig_province)
            fig_city = arg.get("fig_city")
            print(fig_city)
            fig_county = arg.get("fig_county")
            print(fig_county)

            Figure.objects.create(fig_ch_name=fig_ch_name, fig_en_name=fig_en_name, fig_gender=fig_gender,
                                    fig_birthday=fig_birthday, fig_deathday=fig_deathday, fig_day_correction=fig_day_correction,
                                    fig_detail=fig_detail, fig_nationality=fig_nationality, fig_province=fig_province,
                                    fig_city=fig_city, fig_county=fig_county)


            return Response({'msg': "添加成功"}, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "添加失败"}, 500)

    # 按照lit_id查找 然后按照传入的参数修改
    def put(self, request):
        arg = request.data
        try:
            fig_id = arg.get("fig_id")
            fig_ch_name = arg.get("fig_ch_name")
            fig_en_name = arg.get("fig_en_name")
            fig_gender = arg.get("fig_gender")
            # fig_birthday = datetime.strptime(arg.get("fig_birthday", ""), "%Y-%m-%d").date()
            fig_birthday = arg.get("fig_birthday")
            fig_deathday = arg.get("fig_deathday")
            fig_day_correction = arg.get("fig_day_correction")
            fig_detail = arg.get("fig_detail")
            fig_nationality = arg.get("fig_nationality")
            fig_province = arg.get("fig_province")
            fig_city = arg.get("fig_city")
            fig_county = arg.get("fig_county")

            kwargs = {}
            if fig_ch_name:
                kwargs["fig_ch_name"] = fig_ch_name
            if fig_en_name:
                kwargs["fig_en_name"] = fig_en_name
            if fig_gender:
                kwargs["fig_gender"] = fig_gender
            if fig_birthday:
                kwargs["fig_birthday"] = fig_birthday
            if fig_deathday:
                kwargs["fig_deathday"] = fig_deathday
            if fig_day_correction:
                kwargs["fig_day_correction"] = fig_day_correction
            if fig_detail:
                kwargs["fig_detail"] = fig_detail
            if fig_nationality:
                kwargs["fig_nationality"] = fig_nationality
            if fig_province:
                kwargs["fig_province"] = fig_province
            if fig_city:
                kwargs["fig_city"] = fig_city
            if fig_county:
                kwargs["fig_county"] = fig_county

            Figure.objects.filter(fig_id=fig_id).update(**kwargs)

            return Response({'msg': "修改成功"}, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "修改失败"}, 500)

    # 按照lit_id删除 可以批量删除
    def delete(self, request):
        arg = request.GET
        try:
            fig_id_list = arg.get("fig_id_list", "").split(',')
            print(fig_id_list)

            Figure.objects.filter(fig_id__in=fig_id_list).delete()

            return Response({'msg': "删除成功"}, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "删除失败"}, 500)
