from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *
from api.serializers import *
from api.SeleniumBuilder import *
import json

@api_view(['GET', 'POST'])
def test_list(request):
    """
    Liste de tous les tests, ou creer un nouveau test
    """
    if request.method == 'GET':
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TestSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def extension_test_creation(request):
    """
    Creer un nouveau test depuis un enregistrement json de l'extension
    """ 
    if request.method == 'POST':
        data = request.data          
        test = Test()
        test.loadFromRecord(data)
        test.save()
        for step in data['steps']:
            etape = Etape()
            etape.loadFromRecord(test,step)
            etape.save()
            test.etapes.append(etape)
        fichierPyt = SeleniumBuilder(test).obtenir_script()
        file = open(test.titre+".py", "w", encoding='utf-8')
        file.write(fichierPyt)
        file.close()

        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def test_detail(request, pk):
    """
    Get, udpate, ou delete un test specifique
    """
    try:
        test = Test.objects.get(pk=pk)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestSerializer(test)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestSerializer(test, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)