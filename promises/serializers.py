from django.contrib.auth.models import User
from rest_framework import serializers
from promises.models import Promise
from django.db.models import Q
class PromiseSerializer(serializers.ModelSerializer):
	user1 = serializers.ReadOnlyField(source='user1.id')
	def validate(self,value):
		if value['sinceWhen']>value['tilWhen']:
			raise serializers.ValidationError("tilWhen is faster than sinceWhen")
		elif self.context['request'].method == 'POST': 
			if self.context['request'].user == value['user2']:
				raise serializers.ValidationError("can't make promise self")
		return value

	class Meta:
		model = Promise
		fields = ('id', 'created','title','sinceWhen','tilWhen','user1','user2')

class PromiseUpdateSerializer(PromiseSerializer):
	class Meta(PromiseSerializer.Meta):
		read_only_fields = ('user2',)

class UserSerializer(serializers.ModelSerializer):
	promises_as_invitee = serializers.PrimaryKeyRelatedField(many=True, queryset=Promise.objects.all())
	promises_as_inviter = serializers.PrimaryKeyRelatedField(many=True, queryset=Promise.objects.all())
	class Meta:
		model = User
		fields = ('id', 'username', 'promises_as_invitee','promises_as_inviter')

class UserAllSerializer(serializers.ModelSerializer):
	whole_promises = serializers.SerializerMethodField()
	def get_whole_promises(self, obj):
		value=Promise.objects.filter(Q(user1=obj.id) | Q(user2=obj.id)).values('id').distinct()
		value_set=set([entry['id'] for entry in value])
		return value_set
	class Meta:
		model = User
		fields = ('id', 'username', 'whole_promises')