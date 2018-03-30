import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Idioms(models.Model):
    chengyu = models.CharField(_('成语'), max_length=128)
    pinyin = models.CharField(_('拼音'), max_length=128, blank=True, null=True)
    jianpin = models.CharField(_('简拼'), max_length=64, blank=True, null=True)
    jinyi = models.CharField(_('近义'), max_length=512, blank=True, null=True)
    fanyi = models.CharField(_('反义'), max_length=512, blank=True, null=True)
    yongfa = models.TextField(_('用法'), max_length=4096, blank=True, null=True)
    jieshi = models.TextField(_('解释'), max_length=4096, blank=True, null=True)
    chuchu = models.TextField(_('出处'), max_length=4096, blank=True, null=True)
    lizi = models.TextField(_('例子'), max_length=4096, blank=True, null=True)
    xiehouyu = models.CharField(_('谒后语'), max_length=256, blank=True, null=True)
    miyu = models.CharField(_('谜语'), max_length=128, blank=True, null=True)
    gushi = models.TextField(_('成语故事'), max_length=8192, blank=True, null=True)

    class Meta:
        verbose_name = _('成语')
        verbose_name_plural = _('成语')

    def __str__(self):
        return self.chengyu


class AppUser(models.Model):
    id = models.UUIDField(_('用户标识'), primary_key=True, default=uuid.uuid4)
    openid = models.CharField(_('微信OpenId'), max_length=128)
    session_key = models.CharField(_('会话密钥'), max_length=128)
    unionid = models.CharField(_('统一Id'), max_length=128, null=True)
    user_info = models.TextField(_('用户信息'), max_length=512, null=True)
    quizzed = models.ManyToManyField('Idioms', verbose_name=_('已测试的成语'), editable=False)

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __str__(self):
        return self.id.hex
