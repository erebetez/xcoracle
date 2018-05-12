<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="table/tbody">
<flights>
   <xsl:apply-templates/>
</flights>
</xsl:template>

<xsl:template match="tr[@id]">
 <flight>
  <time><xsl:value-of select="td/div/em"/></time>
  <location><xsl:value-of select="td/div/a[@class='lau']"/></location>
  <points><xsl:value-of select="td[@class='pts']"/></points>
  <length><xsl:value-of select="td[@class='km']"/></length>
 </flight>
</xsl:template>

<xsl:template match="text()"/>

</xsl:stylesheet>
