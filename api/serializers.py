from rest_framework import serializers

from .models import Student


# validators
def start_with_r(value):
    if value[0].lower() != 'r':
        raise serializers.ValidationError('Name Must Be start with r')


class StudentSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=100, validators=[start_with_r])  # validators apply here

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(instance.name)
        instance.name = validated_data.get('name', instance.name)
        print(instance.name)
        instance.roll = validated_data.get('roll', instance.roll)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

    # Field Value Validation

    def validate_roll(self, value):
        if value >= 200:
            raise serializers.ValidationError('Seat Full')
        return value

    # Object level Validation
    def validate(self, attrs):
        name = attrs.get('name')
        if name.lower() != 'suyash':
            raise serializers.ValidationError('Name Must be Suyash')
        return attrs


# ModelSerializer for easy serialization in without creating serializer model or writing update and create methods

class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll', 'city']
        # read_only_fields = ['name', 'city'] for read only
        extra_kwargs = {'name': {'read_only': True}}

        # ModelSerializer Validation is same as Serializer Class
