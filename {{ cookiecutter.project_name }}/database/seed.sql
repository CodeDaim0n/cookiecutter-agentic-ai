-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.customers (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  email text NOT NULL,
  phone_number text,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT customers_pkey PRIMARY KEY (id)
);
CREATE TABLE public.order_assignments (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  order_id uuid,
  staff_id uuid,
  role text NOT NULL,
  assigned_at timestamp without time zone DEFAULT now(),
  CONSTRAINT order_assignments_pkey PRIMARY KEY (id),
  CONSTRAINT order_assignments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id),
  CONSTRAINT order_assignments_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.restaurant_staff(id)
);
CREATE TABLE public.order_items (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  order_id uuid,
  item_name text NOT NULL,
  quantity integer NOT NULL,
  notes text,
  CONSTRAINT order_items_pkey PRIMARY KEY (id),
  CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id)
);
CREATE TABLE public.orders (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  customer_id uuid,
  status text CHECK (status = ANY (ARRAY['new'::text, 'preparing'::text, 'ready'::text, 'out_for_delivery'::text, 'delivered'::text, 'cancelled'::text])),
  special_request text,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  staff_id uuid,
  CONSTRAINT orders_pkey PRIMARY KEY (id),
  CONSTRAINT orders_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.restaurant_staff(id),
  CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id)
);
CREATE TABLE public.restaurant_staff (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  role text NOT NULL,
  shift_day text NOT NULL CHECK (shift_day = ANY (ARRAY['Monday'::text, 'Tuesday'::text, 'Wednesday'::text, 'Thursday'::text, 'Friday'::text, 'Saturday'::text, 'Sunday'::text])),
  shift_start time without time zone NOT NULL,
  shift_end time without time zone NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  status text NOT NULL DEFAULT 'available'::text CHECK (status = ANY (ARRAY['available'::text, 'assigned'::text, 'off_shift'::text])),
  CONSTRAINT restaurant_staff_pkey PRIMARY KEY (id)
);