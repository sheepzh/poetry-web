@echo off

REM �뽫�ýű��ƶ��������ʫ��Ŀ¼����ʹ��
REM %1%=ʫ�����
REM %2%=��������

if "%1%"=="" (
echo ������ʫ������
goto entrance
) 

set fileName=%1%.pt

if exist %fileName% (
echo �ļ��Ѵ��ڡ����踲�ǣ�����ʹ����������ɾ�����ļ�
echo del %fileName%
goto entrance
)

REM ʹ��UTF-8
chcp 65001

set firstLine=title:%1%
set nextLine=date:%2%
echo %firstLine% > %fileName%
echo %nextLine% >> %fileName%
start %fileName%

:entrance