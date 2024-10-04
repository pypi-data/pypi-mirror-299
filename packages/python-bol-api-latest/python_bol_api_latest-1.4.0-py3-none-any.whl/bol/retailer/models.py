import json
import sys
from datetime import date
from decimal import Decimal

import dateutil.parser


def _is_str(v):
    if sys.version_info >= (3, 0, 0):
        string_types = str,
    else:
        string_types = basestring,
    return isinstance(v, string_types)


def parse_json(content):
    return json.loads(content, parse_float=Decimal)


class Field(object):
    def parse(self, api, raw_data, instance):
        raise NotImplementedError


class RawField(Field):
    def parse(self, api, raw_data, instance):
        return raw_data


class DecimalField(Field):
    def parse(self, api, raw_data, instance):
        return Decimal(raw_data)


class DateTimeField(Field):
    def parse(self, api, raw_data, instance):
        return dateutil.parser.parse(raw_data)


class DateField(Field):
    def parse(self, api, raw_data, instance):
        parts = raw_data.split("-")
        if len(parts) != 3:
            raise ValueError(raw_data)
        iparts = list(map(int, parts))
        return date(*iparts)


class ModelField(Field):
    def __init__(self, model):
        self.model = model

    def parse(self, api, xml, instance):
        return self.model.parse(api, xml)


class BaseModel(object):
    @classmethod
    def parse(cls, api, content):
        m = cls()
        if _is_str(content):
            m.raw_content = content
            m.raw_data = parse_json(content)
        else:
            m.raw_content = None
            m.raw_data = content
        return m


class Model(BaseModel):
    @classmethod
    def parse(cls, api, content):
        m = super(Model, cls).parse(api, content)
        for tag, v in m.raw_data.items():
            field = getattr(m.Meta, tag, RawField())
            setattr(m, tag, field.parse(api, v, m))
        return m


class ModelList(list, BaseModel):
    @classmethod
    def parse(cls, api, content):
        ml = super(ModelList, cls).parse(api, content)
        items_key = getattr(ml.Meta, "items_key", None)
        if items_key:
            items = ml.raw_data.get(items_key)
        else:
            items = ml.raw_data
        if items:
            for item in items:
                ml.append(ml.Meta.item_type.parse(api, item))
        return ml


class BillingDetails(Model):
    class Meta:
        pass


class ShipmentDetails(Model):
    class Meta:
        pass


class PickUpPoint(Model):
    class Meta:
        pass


class PickUpPoints(ModelList):
    class Meta:
        item_type = PickUpPoint


class Fulfilment(Model):

    class Meta:
        latestDeliveryDate = DateField()
        expiryDate = DateField()
        exactDeliveryDate = DateField()
        pickUpPoints = ModelField(PickUpPoints)


class Offer(Model):
    class Meta:
        pass


class Product(Model):
    class Meta:
        pass


class Country(Model):
    class Meta:
        pass


class Countries(ModelList):
    class Meta:
        item_type = Country


class PeriodData(Model):
    class Meta:
        pass


class TotalData(Model):
    class Meta:
        pass


class Period(Model):
    class Meta:
        countries = ModelField(Countries)
        total = RawField()
        period = ModelField(PeriodData)


class Periods(ModelList):
    class Meta:
        item_type = Period


class Insight(Model):
    class Meta:
        countries = ModelField(Countries)
        periods = ModelField(Periods)


class Insights(ModelList):
    class Meta:
        item_type = Insight
        items_key = "offerInsights"


class Score(Model):
    class Meta:
        pass


class Norm(Model):
    class Meta:
        pass


class Details(Model):
    class Meta:
        period = ModelField(PeriodData)
        score = ModelField(Score)
        norm = ModelField(Norm)


class PerformanceIndicator(Model):
    class Meta:
        details = ModelField(Details)


class PerformanceIndicators(ModelList):
    class Meta:
        item_type = PerformanceIndicator
        items_key = "performanceIndicators"


class ProductRank(Model):
    class Meta:
        pass


class ProductRanks(ModelList):
    class Meta:
        item_type = ProductRank
        items_key = "ranks"


class SalesForecast(Model):
    class Meta:
        countries = ModelField(Countries)
        periods = ModelField(Periods)
        total = ModelField(TotalData)


class RelatedSearchTerm(Model):
    class Meta:
        pass


class RelatedSearchTerms(ModelList):
    class Meta:
        item_type = RelatedSearchTerm


class SearchTermsData(Model):
    class Meta:
        countries = ModelField(Countries)
        periods = ModelField(Periods)
        relatedSearchTerms = ModelField(RelatedSearchTerms)


class SearchTerms(Model):
    class Meta:
        searchTerms = ModelField(SearchTermsData)


class additionalService(Model):
    class Meta:
        pass


class additionalServices(ModelList):
    class Meta:
        item_type = additionalService


class OrderItem(Model):
    class Meta:
        fulfilment = ModelField(Fulfilment)
        offer = ModelField(Offer)
        product = ModelField(Product)
        additionalServices = ModelField(additionalServices)
        offerPrice = DecimalField()
        transactionFee = DecimalField()
        latestChangedDateTime = DateTimeField()


class OrderItems(ModelList):
    class Meta:
        item_type = OrderItem


class Order(Model):
    class Meta:
        orderItems = ModelField(OrderItems)
        orderPlacedDateTime = DateTimeField()
        shipmentDetails = ModelField(ShipmentDetails)
        billingDetails = ModelField(BillingDetails)


class Orders(ModelList):
    class Meta:
        item_type = Order
        items_key = "orders"


class ShipmentItem(Model):
    class Meta:
        orderDate = DateTimeField()
        latestDeliveryDate = DateTimeField()


class ShipmentItems(ModelList):
    class Meta:
        item_type = ShipmentItem


class Transport(Model):
    class Meta:
        pass


class Shipment(Model):
    class Meta:
        shipmentDateTime = DateTimeField()
        shipmentItems = ModelField(ShipmentItems)
        transport = ModelField(Transport)


class Shipments(ModelList):
    class Meta:
        item_type = Shipment
        items_key = "shipments"


class Link(Model):
    class Meta:
        pass


class Links(ModelList):
    class Meta:
        item_type = Link


class ProcessStatus(Model):
    class Meta:
        createTimestamp = DateTimeField()
        links = ModelField(Links)


class ProcessStatuses(ModelList):
    class Meta:
        items_key = "processStatuses"
        item_type = ProcessStatus


class Invoice(Model):
    class Meta:
        pass


class Invoices(ModelList):
    class Meta:
        item_type = Invoice
        items_key = "invoiceListItems"


class InvoiceSpecificationItem(Model):
    class Meta:
        pass


class InvoiceSpecification(ModelList):
    class Meta:
        item_type = InvoiceSpecificationItem
        items_key = "invoiceSpecification"


class LabelPrice(Model):
    class Meta:
        totalPrice = DecimalField()


class PackageRestrictions(Model):
    class Meta:
        pass


class HandoverDetails(Model):
    class Meta:
        latestHandoverDateTime = DateTimeField()


class Labels(Model):

    class Meta:
        validUntilDate = DateField()
        labelPrice = ModelField(LabelPrice)
        packageRestrictions = ModelField(PackageRestrictions)
        handoverDetails = ModelField(HandoverDetails)


class ShippingLabels(ModelList):

    class Meta:
        items_key = "deliveryOptions"
        item_type = Labels


class VisibleCountryCode(Model):

    class Meta:
        pass


class VisibleCountriesCodes(ModelList):

    class Meta:
        item_type = VisibleCountryCode


class Store(Model):

    class Meta:
        visible = ModelField(VisibleCountriesCodes)


class Stock(Model):

    class Meta:
        pass


class Condition(Model):

    class Meta:
        pass


class BundlePrice(Model):

    class Meta:
        unitPrice = DecimalField()


class BundlePrices(ModelList):

    class Meta:
        item_type = BundlePrice


class Prices(Model):

    class Meta:
        bundlePrices = ModelField(BundlePrices)


class NotPublishableReason(Model):

    class Meta:
        pass


class NotPublishableReasons(ModelList):

    class Meta:
        item_type = NotPublishableReason


class OffersResponse(Model):

    class Meta:
        pricing = ModelField(Prices)
        fulfilment = ModelField(Fulfilment)
        store = ModelField(Store)
        stock = ModelField(Stock)
        condition = ModelField(Condition)
        notPublishableReasons = ModelField(NotPublishableReasons)


class ProcessingResult(Model):

    class Meta:
        processingDateTime = DateTimeField()


class ProcessingResults(ModelList):

    class Meta:
        item_type = ProcessingResult


class ReturnReason(Model):

    class Meta:
        pass


class CustomerDetails(Model):
    class Meta:
        pass


class ReturnItemsDetail(Model):

    class Meta:
        returnReason = ModelField(ReturnReason)
        processingResults = ModelField(ProcessingResults)
        customerDetails = ModelField(CustomerDetails)


class ReturnItemsDetails(ModelList):

    class Meta:
        item_type = ReturnItemsDetail


class SingleReturnItem(Model):

    class Meta:
        registrationDateTime = DateTimeField()
        returnItems = ModelField(ReturnItemsDetails)


class ReturnItem(Model):

    class Meta:
        returnItems = ModelField(ReturnItemsDetails)
        registrationDateTime = DateTimeField()


class ReturnItems(ModelList):

    class Meta:
        items_key = 'returns'
        item_type = ReturnItem


class Line(Model):
    class Meta:
        pass


class Lines(ModelList):
    class Meta:
        item_type = Line

class InvalidLine(Model):
    class Meta:
        pass


class InvalidLines(ModelList):
    class Meta:
        item_type = InvalidLine

class DestinationWarehouse(Model):
    class Meta:
        pass

class DeliveryInformation(Model):
    class Meta:
        destinationWarehouse = ModelField(DestinationWarehouse)
        expectedDeliveryDate = DateField()

class Address(Model):
    class Meta:
        pass

class PickupAppointment(Model):
    class Meta:
        address = ModelField(Address)

class TimeSlot(Model):
    class Meta:
        fromDateTime = DateTimeField()
        untilDateTime = DateTimeField()


class TimeSlots(ModelList):
    class Meta:
        item_type = TimeSlot
        items_key = "timeSlots"

class LoadCarrier(Model):
    class Meta:
        transportStateUpdateDateTime = DateTimeField()


class LoadCarriers(ModelList):
    class Meta:
        item_type = LoadCarrier

class StateTransition(Model):
    class Meta:
        stateDateTime = DateTimeField()


class StateTransitions(ModelList):
    class Meta:
        item_type = StateTransition

class Replenishment(Model):
    class Meta:
        lines = ModelField(Lines)
        invalidLines = ModelField(InvalidLines)
        creationDateTime = DateTimeField()
        deliveryInformation = ModelField(DeliveryInformation)
        pickupAppointment = ModelField(PickupAppointment)
        pickupTimeSlot = ModelField(TimeSlot)
        pickupDateTime = DateTimeField()
        loadCarriers = ModelField(LoadCarriers)
        stateTransitions = ModelField(StateTransitions)

class Replenishments(ModelList):
    class Meta:
        item_type = Replenishment
        items_key = "replenishments"

class Inventory(Model):
    class Meta:
        pass

class Inventories(ModelList):
    class Meta:
        item_type = Inventory
        items_key = "inventory"

class RejectionError(Model):
    class Meta:
        pass

class RejectionErrors(ModelList):
    class Meta:
        item_type = RejectionError

class RejectedAttribute(Model):
    class Meta:
        rejectionErrors = ModelField(RejectionErrors)

class RejectedAttributes(ModelList):
    class Meta:
        item_type = RejectedAttribute

class ProductContent(Model):
    class Meta:
        rejectedAttributes = ModelField(RejectedAttributes)

class ProductContents(ModelList):
    class Meta:
        item_type = ProductContent
        items_key = "productContents"
