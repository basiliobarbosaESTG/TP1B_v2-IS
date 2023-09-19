--USE OPENXMLTesting
--GO

--DECLARE @XML AS XML, @hDoc AS INT, @SQL NVARCHAR (MAX)

--SELECT @XML = XMLData FROM XMLwithOpenXML

--EXEC sp_xml_preparedocument @hDoc OUTPUT, @XML

--SELECT CustomerID, CustomerName, Address
--FROM OPENXML(@hDoc, 'ROOT/Customers/Customer')
--WITH 
--(
--CustomerID [varchar](50) '@CustomerID',
--CustomerName [varchar](100) '@CustomerName',
--Address [varchar](100) 'Address'
--)

--EXEC sp_xml_removedocument @hDoc
--GO

--USE xmldata --base de dados usada
--GO

DECLARE @XML AS XML, @hDoc AS INT, @SQL NVARCHAR (MAX)

SELECT @XML = XMLData FROM xmldata

EXEC sp_xml_preparedocument @hDoc OUTPUT, @XML

SELECT name, sex
FROM OPENXML(@hDoc, 'athletes/atlethe')
WITH (
name [varchar](50) '@name',
sex [varchar](100) 'sex'
)

EXEC sp_xml_removedocument @hDoc
--GO