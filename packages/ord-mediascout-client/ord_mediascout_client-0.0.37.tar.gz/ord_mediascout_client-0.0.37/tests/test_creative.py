from ord_mediascout_client import (
    CampaignType,
    CreateCreativeRequest,
    CreativeForm,
    CreativeMediaDataItem,
    CreativeStatus,
    CreativeTextDataItemWebApiDto,
    GetCreativesWebApiDto,
)
from ord_mediascout_client.models import FileType


def test_create_mediadata_creative(client):
    request_data = CreateCreativeRequest(
        finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
        initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
        type=CampaignType.CPM,
        form=CreativeForm.Banner,
        advertiserUrls=['https://clisite1.ru/', 'https://clisite2.ru/'],
        description='Test mediadata creative 333',
        targetAudience='',
        isSelfPromotion=False,
        isNative=False,
        isSocial=False,
        okvedCodes=['01.02', '01.03'],
        mediaData=[
            CreativeMediaDataItem(
                fileName='logo.svg',
                fileType=FileType.Image,
                # fileContentBase64="string",
                srcUrl='https://kokoc.com/local/templates/kokoc/web/images/logo/logo.svg',
                description='Тестовый баннер 333',
                isArchive=False,
            )
        ],
    )

    response_data = client.create_creative(request_data)

    assert response_data.id is not None


def test_create_textdata_creative(client):
    request_data = CreateCreativeRequest(
        finalContractId='CTiwhIpoQ_F0OEPpKj8vWKGg',
        initialContractId='CTKLAzsvgYREmK0unGXLsCTg',
        type=CampaignType.CPM,
        form=CreativeForm.Text,
        advertiserUrls=['https://clisite1.ru/', 'https://clisite2.ru/'],
        description='Test textdata creative 555',
        targetAudience='',
        isSelfPromotion=False,
        isNative=False,
        isSocial=False,
        okvedCodes=['01.05'],
        textData=[CreativeTextDataItemWebApiDto(textData='Creative 555 text data test')],
    )

    response_data = client.create_creative(request_data)

    assert response_data.id is not None


def test_get_creatives(client):
    request_data = GetCreativesWebApiDto(status=CreativeStatus.Active)

    response_data = client.get_creatives(request_data)

    for creative in response_data:
        assert creative.id is not None
