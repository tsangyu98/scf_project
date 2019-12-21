from rest_framework import serializers

from roast.models import Spit


class SpitModelSerializer(serializers.ModelSerializer):
    '''吐槽列表和发布吐槽'''
    # parent=serializers.PrimaryKeyRelatedField(label='parent',required=False,read_only=True,many=True)
    class Meta:
        model=Spit
        # fields='__all__'
        exclude=('nickname','avatar')
        extra_kwargs={
            # 'avatar':{'required':False},
            'userid':{'required':False},
            # 'nickname':{'required':False},
            'parent':{'required':False},
        }
    def validate(self, attrs):
        '''教研数据'''

        parent = attrs.get('attrs')
        if parent:
            try:
                spit=Spit.objects.get(id=parent)
            except Exception as e :
                raise serializers.ValidationError('parent')
        return attrs

class SpitTModelSerializer(serializers.ModelSerializer):
    '''吐槽列表和发布吐槽'''
    success=serializers.SerializerMethodField(read_only=True,label='成不成功')
    # user_a_c = serializers.SerializerMethodField(read_only=True)
    # def get_user_a_c(self, obj):
    #     return
    def get_success(self,obj):
        obj=True
        return obj
    class Meta:
        model=Spit
        fields=("content",'success','collected')
        extra_kwargs = {
            'collected':{'write_only':True},
            "content":{'read_only':True}
        }

class SpitCModelSerializer(serializers.ModelSerializer):
    '''吐槽列表和发布吐槽'''
    success=serializers.SerializerMethodField(read_only=True,label='成不成功')
    def get_success(self,obj):
        obj=True
        return obj
    class Meta:
        model=Spit
        fields=("content",'success','hasthumbup','thumbup')
        extra_kwargs = {
            'hasthumbup':{'write_only':True},
            'thumbup': {'write_only': True},
            "content": {'read_only': True}
        }
