import json
import requests
from requests.models import Response

from .models import (
    Invoice,
    Invoices,
    InvoiceSpecification,
    Order,
    Orders,
    ProcessStatus,
    ProcessStatuses,
    Shipment,
    Shipments,
    ShippingLabels,
    OffersResponse,
    ReturnItems,
    SingleReturnItem,
    Replenishment,
    Replenishments,
    TimeSlots,
    Inventories,
    ProductContents,
    Insights,
    PerformanceIndicators,
    ProductRanks,
    SalesForecast,
    SearchTerms
)

__all__ = ["RetailerAPI"]


class MethodGroup(object):
    def __init__(self, api, group, base_type="retailer"):
        self.api = api
        self.group = group
        self.base_type = base_type

    def request(self, method, path="", params={}, **kwargs):
        uri = path
        base = self.base_type+"-demo" if self.api.demo else self.base_type

        uri = "/{base}/{group}{path}".format(
            base=base,
            group=self.group,
            path=("/{}".format(path) if path else ""),
        )
        return self.api.request(method, uri, params=params, **kwargs)


class OrderMethods(MethodGroup):
    def __init__(self, api):
        super(OrderMethods, self).__init__(api, "orders")

    def list(self, fulfilment_method=None, page=None, status=None, change_interval_minute=None, latest_change_date=None):
        params = {}
        if fulfilment_method:
            params["fulfilment-method"] = fulfilment_method
        if page is not None:
            params["page"] = page
        if status:
            params["status"] = status
        if change_interval_minute:
            params["change-interval-minute"] = change_interval_minute
        if latest_change_date:
            params["latest-change-date"] = latest_change_date

        resp = self.request("GET", params=params)
        return Orders.parse(self.api, resp.text)

    def get(self, order_id):
        resp = self.request("GET", path=order_id)
        return Order.parse(self.api, resp.text)

    def ship_order_item(
        self,
        order_item_id,
        shipment_reference,
        shipping_label_id=None,
        transporter_code=None,
        track_and_trace=None,
    ):
        payload = {}
        orderItems = [
            {
                "orderItemId": order_item_id
            }
        ]
        payload["orderItems"] = orderItems
        payload["shipmentReference"] = shipment_reference
        if shipping_label_id:
            payload["shippingLabelId"] = shipping_label_id
        else:
            if transporter_code:
                payload.setdefault("transport", {})[
                    "transporterCode"
                ] = transporter_code
            if track_and_trace:
                payload.setdefault("transport", {})[
                    "trackAndTrace"
                ] = track_and_trace
        resp = self.request(
            "PUT", path="shipment", json=payload
        )
        return ProcessStatus.parse(self.api, resp.text)

    def cancel_order_item(self, order_item_id, reason_code):
        payload = {
            "orderItems": [
                {
                    "orderItemId": order_item_id,
                    "reasonCode": reason_code
                }
            ]
        }
        resp = self.request(
            "PUT", path="cancellation", json=payload
        )
        return ProcessStatus.parse(self.api, resp.text)


class ShipmentMethods(MethodGroup):
    def __init__(self, api):
        super(ShipmentMethods, self).__init__(api, "shipments")

    def list(self, fulfilment_method=None, page=None, order_id=None):
        params = {}
        if fulfilment_method:
            params["fulfilment-method"] = fulfilment_method
        if page is not None:
            params["page"] = page
        if order_id:
            params["order_id"] = order_id
        resp = self.request("GET", params=params)
        return Shipments.parse(self.api, resp.text)

    def get(self, shipment_id):
        resp = self.request("GET", path=str(shipment_id))
        return Shipment.parse(self.api, resp.text)


class ProcessStatusMethods(MethodGroup):
    def __init__(self, api):
        super(ProcessStatusMethods, self).__init__(api, "process-status", "shared")

    def get(self, entity_id, event_type, page=None):
        params = {"entity-id": entity_id, "event-type": event_type}
        if page:
            params["page"] = page
        resp = self.request("GET", params=params)
        return ProcessStatuses.parse(self.api, resp.text)

    def getById(self, process_id):
        resp = self.request("GET", path=str(process_id))
        return ProcessStatus.parse(self.api, resp.text)

    def getByIds(self, process_ids):
        if not type(process_ids) is list:
            return {}
        process_id_dict = {
            "processStatusQueries": []
        }
        process_statuses = process_id_dict["processStatusQueries"]
        for process_id in process_ids:
            process_statuses.append({"processStatusId": process_id})
        resp = self.request("POST", json=process_id_dict)
        return ProcessStatuses.parse(self.api, resp.text)


class InvoiceMethods(MethodGroup):
    def __init__(self, api):
        super(InvoiceMethods, self).__init__(api, "invoices")

    def list(self, period_start=None, period_end=None):
        params = {}
        if period_start:
            params.update({'period-start-date':period_start})
        if period_end:
            params.update({'period-end-date':period_end})
        resp = self.request("GET", params=params)
        return Invoices.parse(self.api, resp.text)

    def get(self, invoice_id):
        resp = self.request("GET", path=str(invoice_id))
        return Invoice.parse(self.api, resp.text)

    def get_specification(self, invoice_id, page=None):
        params = {}
        if page is not None:
            params["page"] = page
        resp = self.request(
            "GET", path="{}/specification".format(invoice_id), params=params
        )
        return InvoiceSpecification.parse(self.api, resp.text)


class TransportMethods(MethodGroup):

    def __init__(self, api):
        super(TransportMethods, self).__init__(api, 'transports')

    def update(self, transport_id, transporter_code, track_and_trace):
        payload = {
            'transporterCode': transporter_code,
            'trackAndTrace': track_and_trace,
        }
        response = self.request('PUT', '{}'.format(transport_id), json=payload)
        return ProcessStatus.parse(self.api, response.text)


class ShippingLabelsMethods(MethodGroup):

    def __init__(self, api):
        super(ShippingLabelsMethods, self).__init__(
            api,
            'shipping-labels')

    def getDeliveryOptions(self, orderitems_list):
        if orderitems_list and isinstance(orderitems_list, list):
            payload = {
                "orderItems" : orderitems_list
                }
            response = self.request("POST", path="delivery-options", json=payload)
            return ShippingLabels.parse(self.api, response.text)

    def createShippingLabel(self, orderitems_list, label_id):
        if orderitems_list and isinstance(orderitems_list, list) and label_id:
            payload = {
                "orderItems" : orderitems_list,
                "shippingLabelOfferId" : label_id
            }
            response = self.request("POST", json=payload)
            return ProcessStatus.parse(self.api, response.text)

    def getShippingLabel(self, shipping_label_id):
        headers = {
            "accept": "application/vnd.retailer.v10+pdf"
        }
        response = self.request('GET', path=str(shipping_label_id), headers=headers)
        return response

class OffersMethods(MethodGroup):

    def __init__(self, api):
        super(OffersMethods, self).__init__(api, 'offers')

    def createSingleOffer(self, data):
        first_level_fields = ['ean', 'condition',
                              'pricing', 'stock', 'fulfilment']
        second_level_fields = {
            'condition': ['name'],
            'pricing': {'bundlePrices': []},
            'stock': ['amount', 'managedByRetailer'],
            'fulfilment': ['method'],
        }

        # Keeping the validation part out of scope for now & just make request
        # And handle response
        response = self.request('POST', json=data)
        return ProcessStatus.parse(self.api, response.text)

    def updateProduct(self, offer_id, data):
        if "fulfilment" not in data:
            # We handle basic validation here as not having fulfilment in data
            # will give error from bol side
            return "{'error': 'Insufficient data provided'}"

        response = self.request('PUT', path='{}'.format(offer_id), json=data)
        return ProcessStatus.parse(self.api, response.text)

    def updateProductPrice(self, offer_id, data):
        response = self.request(
            'PUT', path='{}/price'.format(offer_id), json=data)
        return ProcessStatus.parse(self.api, response.text)

    def updateProductStock(self, offer_id, data):
        response = self.request(
            'PUT', path='{}/stock'.format(offer_id), json=data)
        return ProcessStatus.parse(self.api, response.text)

    def getSingleOffer(self, offer_id):
        response = self.request('GET', path=str(offer_id))
        return OffersResponse.parse(self.api, response.text)

    def requestExportFile(self):
        payload = {
            'format': 'CSV'
        }
        response = self.request('POST', path='export', json=payload)
        return ProcessStatus.parse(self.api, response.text)

    def getOffersFile(self, export_id):
        headers = {
            "accept": "application/vnd.retailer.v10+csv"
        }
        response = self.request('GET', path='export/{}'.format(export_id),
                                headers=headers)
        return response

    def deleteOffers(self, offer_id):
        response = self.request('DELETE', path='{}'.format(offer_id))
        return ProcessStatus.parse(self.api, response.text)


class InsightsMethods(MethodGroup):

    def __init__(self, api):
        super(InsightsMethods, self).__init__(api, 'insights')

    def getOfferInsights(self, offer_id, period, number_of_periods, name):
        if offer_id and period and number_of_periods and name and isinstance(name, list):
            params = {
                'offer-id': offer_id,
                'period': period,
                'number-of-periods': number_of_periods,
                'name': ','.join(name),
            }
            resp = self.request("GET", path="offer", params=params)
            return Insights.parse(self.api, resp.text)

    def getPerformanceIndicators(self, name, year, week):
        if name and isinstance(name, list) and year and week:
            params = {
                'name': ','.join(name),
                'year': year,
                'week': week
            }
            resp = self.request("GET", path="performance/indicator", params=params)
            return PerformanceIndicators.parse(self.api, resp.text)

    def getProductRanks(self, ean, date, type=None, page=1):
        if ean and date:
            params = {'ean': ean, 'date': date}
            if type:
                params["type"] = ','.join(type)
            if page != 1:
                params["page"] = page

            resp = self.request("GET", path="product-ranks", params=params)
            return ProductRanks.parse(self.api, resp.text)

    def getSalesForecast(self, offer_id, weeks_ahead):
        if offer_id and weeks_ahead:
            params = {
                "offer-id": offer_id,
                "weeks-ahead": weeks_ahead
            }
            resp = self.request("GET", path="sales-forecast", params=params)
            return SalesForecast.parse(self.api, resp.text)

    def getSearchTerms(self, search_term, period, number_of_periods, related_search_terms=None):
        if search_term and period and number_of_periods:
            params = {
                "search-term": search_term,
                "period": period,
                "number-of-periods": number_of_periods
            }
            if related_search_terms:
                params["related-search-terms"] = related_search_terms

            resp = self.request("GET", path="search-terms", params=params)
            return SearchTerms.parse(self.api, resp.text)

class ReturnsMethods(MethodGroup):
    def __init__(self, api):
        super(ReturnsMethods, self).__init__(api, "returns")

    def get(self, page=1, handled=False, fulfilment_method="FBR"):
        params = {
            "handled": handled,
            "fulfilment-method": fulfilment_method
        }
        if page != 1:
            params["page"] = page
        resp = self.request("GET", params=params)
        return ReturnItems.parse(self.api, resp.text)

    def create_return(self, data):
        response = self.request('POST', json=data)
        return ProcessStatus.parse(self.api, response.text)

    def getSingle(self, returnId):
        resp = self.request("GET", path=str(returnId))
        return SingleReturnItem.parse(self.api, resp.text)

    def handleReturnItem(self, rmaId, status_reason, qty):
        payload = {"handlingResult": status_reason, "quantityReturned": qty}
        response = self.request("PUT", path=str(rmaId), json=payload)
        return ProcessStatus.parse(self.api, response.text)

class ReplenishmentMethods(MethodGroup):
    def __init__(self, api):
        super(ReplenishmentMethods, self).__init__(api, "replenishments")

    def get(self, **params):
        response = self.request("GET", params=params)
        return Replenishments.parse(self.api, response.text)

    def create(self, params):
        response = self.request("POST", json=params)
        return ProcessStatus.parse(self.api, response.text)

    def getpickupTimeSlots(self,address, numberOfLoadCarriers):
        params = {
            "address" : address,
            "numberOfLoadCarriers" : numberOfLoadCarriers
        }
        response = self.request("POST", path="pickup-time-slots", json=params)
        return TimeSlots.parse(self.api, response.text)

    def getProductLabels(self, labelFormat, products):
        params = {
            "labelFormat" : labelFormat,
            "products" : products
        }

        headers = {
            "accept": "application/vnd.retailer.v10+pdf"
        }
        response = self.request("POST", path="product-labels", headers=headers, json=params)
        return response

    def getById(self, replenishment_id):
        response = self.request("GET", path=str(replenishment_id))
        return Replenishment.parse(self.api, response.text)

    def update(self, replenishment_id, **param):
        response = self.request("PUT", path=str(replenishment_id), json=param)
        return ProcessStatus.parse(self.api, response.text)

    def getLoadCarrierLabels(self, replenishment_id, label_type="WAREHOUSE"):
        headers = {
            "accept": "application/vnd.retailer.v10+pdf"
        }
        response = self.request("GET", path='{}/load-carrier-labels'.format(replenishment_id), headers=headers, json=label_type)
        return response

    def getPickList(self, replenishment_id):
        headers = {
            "accept": "application/vnd.retailer.v10+pdf"
        }
        response = self.request("GET", path='{}/pick-list'.format(replenishment_id), headers=headers)
        return response

class InventoryMethods(MethodGroup):
    def __init__(self, api):
        super(InventoryMethods, self).__init__(api, "inventory")

    def get(self, params={}):
        response = self.request("GET", params=params)
        return Inventories.parse(self.api, response.text)

class ProductContentMethods(MethodGroup):

    def __init__(self,api):
        super(ProductContentMethods, self).__init__(api, "content")

    def sendContent(self, language, content):
        supported_languages = ["nl","nl-BE","fr","fr-BE"]
        if language not in supported_languages:
            raise ValueError("Unsupported language. Only nl, nl-BE, fr, fr-BE are supported")

        if type(content) is dict:
           content = [content]
        elif type(content) is not list:
            raise ValueError("Incorrect type of content sent")

        final_data = {
            "language": language,
            "productContents": content
        }

        response = self.request("POST",path="product",json=final_data)
        return ProcessStatus.parse(self.api, response.text)

    def getValidationReport(self, uploadId):
        response = self.request("GET", path="validation-report/{}".format(uploadId))
        return ProductContents.parse(self.api, response.text)


class RetailerAPI(object):
    def __init__(
        self,
        test=False,
        timeout=None,
        session=None,
        demo=False,
        api_url=None,
        login_url=None,
        refresh_token=None,
    ):
        self.demo = demo
        self.api_url = api_url or "https://api.bol.com"
        self.login_url = login_url or "https://login.bol.com"
        self.timeout = timeout
        self.refresh_token = refresh_token
        self.orders = OrderMethods(self)
        self.shipments = ShipmentMethods(self)
        self.invoices = InvoiceMethods(self)
        self.process_status = ProcessStatusMethods(self)
        self.offers = OffersMethods(self)
        self.labels = ShippingLabelsMethods(self)
        self.returns = ReturnsMethods(self)
        self.replenishments = ReplenishmentMethods(self)
        self.inventory = InventoryMethods(self)
        self.product_content = ProductContentMethods(self)
        self.transports = TransportMethods(self)
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.insights = InsightsMethods(self)


    def login(self, client_id, client_secret):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        resp = self.session.post(
            self.login_url + "/token",
            auth=(client_id, client_secret),
            data=data,
        )
        resp.raise_for_status()
        token = resp.json()
        self.set_access_token(token["access_token"])
        return token

    def refresh_access_token(
        self,
        username,
        password,
        refresh_token=None
    ):

        if refresh_token is None and self.refresh_token is None:
            raise ValueError("No 'refresh_token' provided")

        if refresh_token is None and self.refresh_token is not None:
            refresh_token = self.refresh_token

        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        resp = self.session.post(
            self.login_url + "/token",
            params=params,
            auth=(username, password),
        )
        resp.raise_for_status()
        data = resp.json()
        self.refresh_token = data["refresh_token"]
        self.set_access_token(data["access_token"])
        return data

    def set_access_token(self, access_token):
        self.session.headers.update(
            {
                "Authorization": "Bearer " + access_token,
                "Accept": "application/vnd.retailer.v10+json",
            }
        )

    def request(self, method, uri, params={}, **kwargs):
        request_kwargs = dict(**kwargs)
        request_kwargs.update(
            {
                "method": method,
                "url": self.api_url + uri,
                "params": params,
                "timeout": self.timeout,
            }
        )
        if "json" in request_kwargs:
            if "headers" not in request_kwargs:
                request_kwargs["headers"] = {}
            # If these headers are not added, the api returns a 400
            # Reference:
            #   https://api.bol.com/retailer/public/conventions/index.html
            content_header = "application/vnd.retailer.v10+json"

            request_kwargs["headers"].update({
                "content-type": content_header
            })

        resp = self.session.request(**request_kwargs)
        resp.raise_for_status()
        return resp
